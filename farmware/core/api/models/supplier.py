from django.db import models

class Supplier(models.Model):
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )
    name = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=10)

    def __str__(self) -> str:
        return self.name