from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _

from ..api.models import Organisation, Team

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()

    class Roles(models.TextChoices): # sa: simplify to just admin, worker?
        ADMIN = 'ADMIN', 'Admin'
        OFFICE = 'OFFICE', 'Office'
        TEAM_LEADER = 'TEAM LEADER', 'Team Leader'
        WORKER = 'WORKER', 'Worker'

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        _("role"), 
        max_length=50,
        choices=Roles.choices, 
        default=Roles.WORKER
        )

    teams = models.ManyToManyField(
        Team,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(roles=User.Roles.ADMIN, organisation=self.model.organisation)

class Admin(User):
    objects = AdminManager

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk: self.role = User.Roles.ADMIN

        return super().save(*args, **kwargs)

class Organisation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    owner_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

class OrganisationCode(models.Model):
    org_code = models.CharField(primary_key=True, max_length=16)
    org_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)

class Produce(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

class ProduceVariety(models.Model):
    id = models.AutoField(primary_key=True)
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    variety = models.TextField(max_length=100)

class ProduceQuantitySuffix(models.Model):
    id = models.AutoField(primary_key=True)
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    suffix = models.TextField(max_length=20)
    base_equivalent = models.FloatField()

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=10)

class AreaCode(models.Model):
    area_code = models.TextField(primary_key=True, max_length=50)
    description = models.TextField(max_length=200)

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    variety_id = models.ForeignKey(ProduceVariety, on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey(ProduceQuantitySuffix, on_delete=models.DO_NOTHING)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    date_seeded = models.DateTimeField()
    date_planted = models.DateTimeField()
    date_picked = models.DateTimeField()
    ehd = models.DateTimeField() # earliest harvest date
    date_completed = models.DateTimeField()
    area_code = models.ForeignKey(AreaCode, on_delete=models.DO_NOTHING)

class StockPickers(models.Model):
    id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    phone_number = models.TextField(max_length=10)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

class OrderStock(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    stock_id = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey(ProduceQuantitySuffix, on_delete=models.DO_NOTHING)
    invoice_number = models.TextField(max_length=20)