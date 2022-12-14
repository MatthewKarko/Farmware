from django.db import models

class Customer(models.Model):
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )
    name = models.TextField(max_length=50)
    phone_number = models.TextField(max_length=10)

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self) -> str:
        return self.name