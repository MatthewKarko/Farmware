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
    quantity_available = models.FloatField(blank=True, default=0)
    quantity_suffix_id = models.ForeignKey('core_api.ProduceQuantitySuffix', on_delete=models.DO_NOTHING)
    supplier_id = models.ForeignKey('core_api.Supplier', on_delete=models.DO_NOTHING)
    date_seeded = models.DateField(null=True, blank=True)
    date_planted = models.DateField(null=True, blank=True)
    date_picked = models.DateTimeField(null=True, blank=True)
    ehd = models.DateField(null=True, blank=True) # Earliest Harvest Date
    date_completed = models.DateField(null=True, blank=True)
    area_code_id = models.ForeignKey('core_api.AreaCode', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "stock"
        verbose_name_plural = "stock"
        ordering = ['-date_picked']

    def use_available_stock(self, quantity: float):
        self.quantity_available -= quantity
        self.save()

    def refund_available_stock(self, quantity: float):
        self.quantity_available += quantity
        self.save()

    def calculate_native_quantity(
        self, 
        quantity: float, 
        base_equivalent: float
        ) -> float:
        self_base_equivalent = self.quantity_suffix_id.base_equivalent
        return quantity * (base_equivalent / self_base_equivalent)

    def __str__(self) -> str:
        return (f'{self.quantity_available:.2f} (/{self.quantity:.2f}) '
        + f'{self.produce_id} {self.quantity_suffix_id} {self.supplier_id} ' 
        + f'[{self.date_picked.date()}]'    #type: ignore
        )
class StockPickers(models.Model):
    stock_id = models.ManyToManyField(Stock)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)