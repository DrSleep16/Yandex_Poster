import json

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Загружает место из JSON-файла или по ссылке'


    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL или путь к JSON-файлу')


    def handle(self, *args, **options):
        json_url = options['json_url']

        if json_url.startswith('http'):
            response = requests.get(json_url)
            response.raise_for_status()
            payload = response.json()
        else:
            with open(json_url, 'r', encoding='utf-8') as f:
                payload = json.load(f)

        place, created = Place.objects.get_or_create(
            title=payload['title'],
            defaults={
                'short_description': payload.get('description_short', ''),
                'long_description': payload.get('description_long', ''),
                'lat': payload['coordinates']['lat'],
                'lng': payload['coordinates']['lng'],
            }
        )

        if not created:
            place.short_description = payload.get('description_short', '')
            place.long_description = payload.get('description_long', '')
            place.lat = payload['coordinates']['lat']
            place.lng = payload['coordinates']['lng']
            place.save()

        for idx, img_url in enumerate(payload.get('imgs', []), start=1):
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            img_name = img_url.split('/')[-1]
            image = PlaceImage(
                place=place,
                order=idx
            )
            image.image.save(img_name, ContentFile(img_response.content), save=True)

        self.stdout.write(self.style.SUCCESS(f'Место "{place.title}" успешно загружено!'))
