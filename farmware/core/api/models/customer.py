from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    phone_number = models.TextField(max_length=10)