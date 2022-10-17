from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from core.api.models.organisation import Organisation
from ..api.constants import ORG_CODE_LENGTH

class UserManager(BaseUserManager):
    """User Manager."""
    def create_user(self, email, first_name, last_name, organisation, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email: 
            raise ValueError('You must provide an email address.')

        if not organisation:
            raise ValueError('You must provide an organisation.')

        if type(organisation) == str:
            if organisation.isdigit() and len(organisation) != ORG_CODE_LENGTH:
                raise ValueError('Invalid organisation code.')

            organisation = Organisation.objects.filter(code=organisation).first()

            if organisation is None:
                raise ValueError('Organisation does not exist.')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # TODO: delete once in production / email verification is implemented.
        extra_fields.setdefault('is_active', True)

        email = self.normalize_email(email)
        user: User = self.model(
            email=email, 
            first_name=first_name, 
            last_name=last_name, 
            organisation=organisation,
            password=password, 
            **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(
        self, 
        email, 
        first_name, 
        last_name, 
        organisation, 
        password=None, 
        **extra_fields
        ):
        return self.create_user(
            email, first_name, last_name, organisation, password, 
            role=User.Roles.ORGANISATION_ADMIN,
            **extra_fields
            )

    def create_superuser(self, email, first_name, last_name, organisation, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_admin(email, first_name, last_name, organisation, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    class Roles(models.IntegerChoices):
        ORGANISATION_ADMIN = 000, 'Organisation Admin'
        ADMIN              = 100, 'Admin'
        TEAM_LEADER        = 200, 'Team Leader'
        OFFICE             = 300, 'Office'
        WORKER             = 400, 'Worker'

    objects = UserManager()

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)

    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )

    role = models.SmallIntegerField(
        _("role"), 
        choices=Roles.choices, 
        default=Roles.WORKER
        )

    teams = models.ManyToManyField(
        'core_api.Team',
        blank=True
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'organisation']

    def get_users(self):
        return User.objects.filter(organisation__code=self.organisation.code)