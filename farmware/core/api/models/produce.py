from django.db import models


class Produce(models.Model):
    """Produce.

    Example:
     - organisation: 000000
     - name: Lettuce
    """
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )
    name = models.TextField(max_length=100)

    class Meta:
        verbose_name = "produce"
        verbose_name_plural = "produce"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'organisation'], 
                name='unique_name_organisation_combination'
            )
        ]

    def __str__(self) -> str:
        return str(self.name)

class ProduceVariety(models.Model):
    """Produce Variety.
    
    Example:
     - produce_id: 1
     - variety: Red Coral
    """
    produce_id = models.ForeignKey(Produce, on_delete=models.CASCADE)
    variety = models.TextField(max_length=100)

    class Meta:
        verbose_name = "produce variety"
        verbose_name_plural = "produce varieties"

    def __str__(self) -> str:
        return str(self.variety)

class ProduceQuantitySuffix(models.Model):
    """Produce Quantity Suffix.
    
    Example:
     - produce_id: 1
     - suffix: Heads
     - base_equivalent: 1.0

    Example (base_equivalent):
     - Base is Heads
     - Another suffix is Boxes
     - base_equivalent would be 10.0, i.e., there are 10 Heads in a Box
    """
    produce_id = models.ForeignKey(Produce, on_delete=models.CASCADE)
    suffix = models.TextField(max_length=20)
    base_equivalent = models.FloatField()

    class Meta:
        verbose_name = "produce quantity suffix"
        verbose_name_plural = "produce quantity suffixes"

    def __str__(self) -> str:
        return str(self.suffix)