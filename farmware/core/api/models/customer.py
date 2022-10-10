from django.db import models

class Customer(models.Model):
    name = models.TextField(max_length=50)
    phone_number = models.TextField(max_length=10)

    def __str__(self) -> str:
        return self.name