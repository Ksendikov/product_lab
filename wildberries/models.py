from django.db import models


class Card(models.Model):
    article = models.PositiveBigIntegerField(
        unique=True
    )
    brand = models.CharField(
        max_length=100,
    )
    title = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.brand

    class Meta:
        ordering = ('article', )
