from django.db import models

class Supplier(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=10)