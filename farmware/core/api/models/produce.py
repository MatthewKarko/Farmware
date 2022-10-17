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
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    variety = models.TextField(max_length=100)

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
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    suffix = models.TextField(max_length=20)
    base_equivalent = models.FloatField()

    def __str__(self) -> str:
        return str(self.suffix)