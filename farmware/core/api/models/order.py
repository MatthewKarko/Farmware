from django.db import models

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('core_api.Customer', on_delete=models.DO_NOTHING)

class OrderStock(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    stock_id = models.ForeignKey('core_api.Stock', on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey('core_api.ProduceQuantitySuffix', on_delete=models.DO_NOTHING)
    invoice_number = models.TextField(max_length=20)