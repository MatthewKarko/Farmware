from django.db import models
from .. import constants

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
        primary_key=True
        )

    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name + ' [' + self.code + ']'