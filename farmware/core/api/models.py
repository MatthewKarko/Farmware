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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    owner_id = models.ForeignKey('core_user.User', on_delete=models.DO_NOTHING, related_name="+")

    code = models.CharField(
        max_length=constants.ORG_CODE_LENGTH, 
        default=generate_random_org_code, 
        unique=True
        )

class Team(models.Model):
    category = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100, default=category.name)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )

class OrganisationCode(models.Model):
    org_code = models.CharField(primary_key=True, max_length=16)
    org_id = models.ForeignKey(Organisation, on_delete=models.DO_NOTHING)

class Produce(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

class ProduceVariety(models.Model):
    id = models.AutoField(primary_key=True)
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    variety = models.TextField(max_length=100)

class ProduceQuantitySuffix(models.Model):
    id = models.AutoField(primary_key=True)
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    suffix = models.TextField(max_length=20)
    base_equivalent = models.FloatField()

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=10)

class AreaCode(models.Model):
    area_code = models.TextField(primary_key=True, max_length=50)
    description = models.TextField(max_length=200)

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    variety_id = models.ForeignKey(ProduceVariety, on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey(ProduceQuantitySuffix, on_delete=models.DO_NOTHING)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    date_seeded = models.DateTimeField()
    date_planted = models.DateTimeField()
    date_picked = models.DateTimeField()
    ehd = models.DateTimeField() # earliest harvest date
    date_completed = models.DateTimeField()
    area_code = models.ForeignKey(AreaCode, on_delete=models.DO_NOTHING)

class StockPickers(models.Model):
    id = models.AutoField(primary_key=True)
    stock_id = models.ManyToManyField(Stock)
    user_id = models.ForeignKey('core_user.User', on_delete=models.DO_NOTHING)

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    phone_number = models.TextField(max_length=10)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

class OrderStock(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    stock_id = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey(ProduceQuantitySuffix, on_delete=models.DO_NOTHING)
    invoice_number = models.TextField(max_length=20)