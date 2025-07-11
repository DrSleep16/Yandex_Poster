from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


MAX_HEIGHT = 200
MAX_WIDTH = 300


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    short_description = HTMLField('Короткое описание', blank=True, null=True)
    long_description = HTMLField('Длинное описание', blank=True, null=True)
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images', verbose_name='Место')
    image = models.ImageField(upload_to='places_images', verbose_name='Картинка')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок', db_index=True)

    def get_preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: {}px; max-width: {}px;" />', self.image.url, MAX_HEIGHT, MAX_WIDTH)
        return ""

    get_preview.short_description = 'Превью'

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.place.title} - {self.order}'
