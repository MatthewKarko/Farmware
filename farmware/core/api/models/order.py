from unittest.util import _MAX_LENGTH
from django.db import models

class Order(models.Model):
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )
    customer_id = models.ForeignKey('core_api.Customer', on_delete=models.DO_NOTHING)
    invoice_number = models.TextField(max_length=20, default='000000') # todo: set this based on order id

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

class OrderStock(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    stock_id = models.ForeignKey('core_api.Stock', on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey('core_api.ProduceQuantitySuffix', on_delete=models.DO_NOTHING)