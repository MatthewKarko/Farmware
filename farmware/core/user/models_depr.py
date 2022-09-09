# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# from ..api.models import Organisation, Role, Team


# class UserManager(BaseUserManager):

#     def create_user(self, username, email, password=None, **kwargs):
#         print('KWARGS:', kwargs)
#         """Create and return a `User` with an email, phone number, username and password."""
#         if username is None:
#             raise TypeError('Users must have a username.')
#         if email is None:
#             raise TypeError('Users must have an email.')

#         user = self.model(username=username, email=self.normalize_email(email), **kwargs)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_superuser(self, username, email, password):
#         """
#         Create and return a `User` with superuser (admin) permissions.
#         """
#         if password is None:
#             raise TypeError('Superusers must have a password.')
#         if email is None:
#             raise TypeError('Superusers must have an email.')
#         if username is None:
#             raise TypeError('Superusers must have an username.')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)

#         return user

# class User(AbstractBaseUser, PermissionsMixin):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     username = models.CharField(db_index=True, max_length=255, unique=True)

#     email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)

#     organisation = models.ForeignKey(
#         Organisation,
#         on_delete=models.CASCADE
#     )

#     role = models.ForeignKey(
#         Role,
#         on_delete=models.PROTECT,
#     )

#     teams = models.ManyToManyField(
#         Team
#     )

#     is_active = models.BooleanField(default=True)

#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     objects = UserManager()

#     def __str__(self):
#         return f"{self.email}"
