from django.db import models


### ORDER #####################################################################
class Order(models.Model):
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
        )
    customer_id = models.ForeignKey(
        'core_api.Customer', on_delete=models.DO_NOTHING
        )
    invoice_number = models.TextField(max_length=20, blank=True)
    order_date = models.DateTimeField()
    completion_date = models.DateTimeField()

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self) -> str:
        return (f'[{self.invoice_number}] {self.customer_id.name}{self.order_date}'
        )
###############################################################################


### ORDER ITEM ################################################################
class OrderItem(models.Model):
    """An produce item within an order."""
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    produce_id = models.ForeignKey(
        'core_api.Produce', on_delete=models.DO_NOTHING
        )
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey(
        'core_api.ProduceQuantitySuffix', on_delete=models.DO_NOTHING
        )

    class Meta:
        verbose_name = "order item"
        verbose_name_plural = "order items"

    def __str__(self) -> str:
        return f'{self.quantity:,} {self.quantity_suffix_id.suffix} {self.produce_id.name}'
###############################################################################


### ORDER ITEM STOCK LINK #####################################################
class OrderItemStockLink(models.Model):
    """The stock belonging to an produce item within an order."""
    order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    quantity = models.FloatField()
    quantity_suffix_id = models.ForeignKey(
        'core_api.ProduceQuantitySuffix', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "order item stock link"
        verbose_name_plural = "order item stock links"
###############################################################################