from django.db import models

class Supplier(models.Model):
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )
    name = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=10)

    class Meta:
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"

    def __str__(self) -> str:
        return self.name