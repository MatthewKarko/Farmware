from django.conf import settings
from django.db import models

class Stock(models.Model):
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )
    produce_id = models.ForeignKey('core_api.Produce', on_delete=models.DO_NOTHING)
    variety_id = models.ForeignKey('core_api.ProduceVariety', on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey('core_api.ProduceQuantitySuffix', on_delete=models.DO_NOTHING)
    supplier_id = models.ForeignKey('core_api.Supplier', on_delete=models.DO_NOTHING)
    date_seeded = models.DateTimeField(null=True, blank=True)
    date_planted = models.DateTimeField(null=True, blank=True)
    date_picked = models.DateTimeField(null=True, blank=True)
    ehd = models.DateTimeField(null=True, blank=True) # Earliest Harvest Date
    date_completed = models.DateTimeField(null=True, blank=True)
    area_code_id = models.ForeignKey('core_api.AreaCode', on_delete=models.DO_NOTHING)

class StockPickers(models.Model):
    stock_id = models.ManyToManyField(Stock)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)