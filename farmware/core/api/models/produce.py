from django.db import models

class Produce(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self) -> str:
        return self.name

class ProduceVariety(models.Model):
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    variety = models.TextField(max_length=100)

    def __str__(self) -> str:
        return self.variety

class ProduceQuantitySuffix(models.Model):
    produce_id = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    suffix = models.TextField(max_length=20)
    base_equivalent = models.FloatField()

    def __str__(self) -> str:
        return self.suffix