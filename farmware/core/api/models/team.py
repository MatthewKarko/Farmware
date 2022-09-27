from django.db import models

class Team(models.Model):
    category = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100, default=category.name)
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )