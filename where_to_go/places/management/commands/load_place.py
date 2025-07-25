import json
import logging
import time

import requests
from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, PlaceImage


logger = logging.getLogger(__name__)


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

        try:
            place, created = Place.objects.update_or_create(
                title=payload['title'],
                defaults={
                    'short_description': payload.get('description_short', ''),
                    'long_description': payload.get('description_long', ''),
                    'lat': payload['coordinates']['lat'],
                    'lng': payload['coordinates']['lng'],
                }
            )
        except MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR(
                f'Найдено несколько мест с названием "{payload["title"]}". '
                'Проверьте уникальность названий!'
            ))
            return

        for idx, img_url in enumerate(payload.get('imgs', []), start=1):
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err:
                logger.error(f'Не удалось загрузить {img_url}: {err}')
                time.sleep(1)
                continue

            img_name = img_url.split('/')[-1]
            PlaceImage.objects.create(
                place=place,
                order=idx,
                image=ContentFile(img_response.content, name=img_name)
            )

        self.stdout.write(self.style.SUCCESS(f'Место "{place.title}" успешно загружено!'))
