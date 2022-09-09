from django.db import models
from django.contrib.auth.models import AbstractUser

from . import constants

import random
import string

def generate_random_org_code() -> str:
    """Generate a k length organisational code."""
    while True:
        code = ''.join(
            random.choices(string.digits, 
            k=constants.ORG_CODE_LENGTH)
            )
        if not Organisation.objects.filter(code=code).exists(): return code

class Organisation(models.Model):
    code = models.CharField(
        max_length=constants.ORG_CODE_LENGTH, 
        default=generate_random_org_code, 
        unique=True, primary_key=True
        )
    name = models.CharField(max_length=100)

class Team(models.Model):
    category = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100, default=category.name)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )