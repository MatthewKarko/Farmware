from django.db import models

class Team(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    organisation = models.ForeignKey(
        'core_api.Organisation',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'organisation'], 
                name='unique_category_organisation_combination'
            )
        ]

    def __str__(self) -> str:
        return self.name