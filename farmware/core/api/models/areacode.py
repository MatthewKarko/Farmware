from django.db import models

class AreaCode(models.Model):
    area_code = models.TextField(primary_key=True, max_length=50)
    description = models.TextField(max_length=200)