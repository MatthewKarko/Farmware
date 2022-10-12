from unittest.util import _MAX_LENGTH
from django.db import models

class Order(models.Model):
    customer_id = models.ForeignKey('core_api.Customer', on_delete=models.DO_NOTHING)
    invoice_number = models.TextField(max_length=20, default='000000') # todo: set this based on order id

class OrderStock(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    stock_id = models.ForeignKey('core_api.Stock', on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey('core_api.ProduceQuantitySuffix', on_delete=models.DO_NOTHING)