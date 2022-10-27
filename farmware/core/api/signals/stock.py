from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from ..models.order import OrderItemStockLink


@receiver(pre_save, sender=OrderItemStockLink)
def remove_stock_from_available(
    sender, 
    instance: OrderItemStockLink, 
    raw,
    using,
    update_fields,
    **kwargs
    ):
    """
    Remove stock quantity from the available quantity once the stock link usage 
    has been created.
    """
    # Get stock
    stock = instance.stock_id

    # Base Equivalent
    base_equivalent = instance.quantity_suffix_id.base_equivalent

    # Add previous quantity back if previous item exists
    if instance.pk is not None:
        previous_item = OrderItemStockLink.objects.get(id=instance.pk)

        # Add stock quantity back
        previous_base_equivalent = previous_item.quantity_suffix_id.base_equivalent

        to_add = stock.calculate_native_quantity(
            previous_item.quantity, previous_base_equivalent
            )

        stock.refund_available_stock(to_add)

    # Convert to quantity relative to stock
    quantity = stock.calculate_native_quantity(
        instance.quantity, base_equivalent
        )

    # Remove new stock quantity
    stock.use_available_stock(quantity)


@receiver(post_delete, sender=OrderItemStockLink)
def add_stock_back_to_available(sender, instance: OrderItemStockLink, using, **kwargs):
    """
    Add stock quantity back to the available quantity once the stock link
    usage has been removed.
    """
    print('add_stock_back_to_available')
    # Get stock
    stock = instance.stock_id

    # Base Equivalent
    base_equivalent = instance.quantity_suffix_id.base_equivalent

    to_add = stock.calculate_native_quantity(
        instance.quantity, base_equivalent
        )

    stock.refund_available_stock(to_add)