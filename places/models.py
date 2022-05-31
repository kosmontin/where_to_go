from django.db import models


# Create your models here.
class Place(models.Model):
    title = models.CharField('Название', max_length=200, db_index=True)
    description_short = models.TextField(
        'Краткое описание', null=True, blank=True)
    description_long = models.TextField(
        'Полное описание', null=True, blank=True)
    lng = models.DecimalField('Долгота',
        max_digits=17, decimal_places=14, null=True, blank=True)
    lat = models.DecimalField('Широта',
        max_digits=17, decimal_places=14, null=True, blank=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title
