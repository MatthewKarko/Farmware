from enum import unique
from django.db import models

class AreaCode(models.Model):
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )
    area_code = models.TextField(max_length=50)
    description = models.TextField(max_length=200)

    class Meta:
        verbose_name = "area code"
        verbose_name_plural = "area codes"

    def __str__(self) -> str:
        return self.area_code