from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200, db_index=True)
    description_short = models.TextField(
        'Краткое описание', null=True, blank=True)
    description_long = models.TextField(
        'Полное описание', null=True, blank=True)
    lng = models.DecimalField(
        'Долгота',max_digits=17, decimal_places=14, null=True, blank=True)
    lat = models.DecimalField(
        'Широта',max_digits=17, decimal_places=14, null=True, blank=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class Photo(models.Model):
    num_order = models.PositiveSmallIntegerField(
        'Порядковый номер', help_text='1 - обложка достопримечательности')

    image = models.ImageField('Картинка', upload_to='uploads/')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии мест'

    def __str__(self):
        return f'{self.num_order} {self.place.title}'
