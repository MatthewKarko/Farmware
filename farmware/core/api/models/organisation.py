from django.db import models
from .. import constants

import random
import string

class Organisation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    owner_id = models.ForeignKey('core_user.User', on_delete=models.DO_NOTHING, related_name="+")

    code = models.CharField(
        max_length=constants.ORG_CODE_LENGTH, 
        default='core_api.generate_random_org_code',
        unique=True
        )

class OrganisationCode(models.Model):
    org_code = models.CharField(primary_key=True, max_length=16)
    org_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)

def generate_random_org_code() -> str:
    """Generate a k length organisational code."""
    while True:
        code = ''.join(
            random.choices(string.digits, 
            k=constants.ORG_CODE_LENGTH)
            )
        if not Organisation.objects.filter(code=code).exists(): return code