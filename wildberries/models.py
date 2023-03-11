from django.db import models


class Product(models.Model):
    article = models.IntegerField(
        verbose_name='article',
    )
    brand = models.CharField(
        verbose_name='brand',
        max_length=100,
    )
    title = models.CharField(
        verbose_name='title',
        max_length=100,
    )

    def __str__(self):
        return self.article

    class Meta:
        ordering = ('article', )
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
