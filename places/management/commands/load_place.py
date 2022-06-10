import os.path
from urllib.parse import unquote, urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from places.models import Photo, Place


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--json_url', help='URL to json file')
        parser.add_argument('--jsons_txt', help='path to file with jsons URLs')

    def handle(self, *args, **options):
        if options['json_url'] and options['jsons_txt']:
            raise CommandError('Warning! Only one parameter at a time!')

        if options['json_url']:
            added_place, is_added_place = get_place_from_json(
                options['json_url'])
            if is_added_place:
                self.stdout.write(
                    self.style.SUCCESS(f'Place {added_place} added'))
            else:
                self.stdout.write(self.style.WARNING('Place already exists'))

        if options['jsons_txt']:
            presented_places, added_places = get_urls_from_file(
                options['jsons_txt'])
            self.stdout.write(
                self.style.SUCCESS(f'Presented {presented_places} places. '
                                   f'Added {added_places} places.'))


def get_place_from_json(url):
    response = requests.get(url)
    response.raise_for_status()
    deserialized_place = response.json()
    added_place, is_added_place = Place.objects.get_or_create(
        title=deserialized_place['title'],
        lng=deserialized_place['coordinates']['lng'],
        defaults={
            'description_short': deserialized_place['description_short'],
            'description_long': deserialized_place['description_long'],
            'lat': deserialized_place['coordinates']['lat'],
        },
    )
    if is_added_place:
        for image_url in deserialized_place['imgs']:
            image_filename = os.path.basename(
                unquote(urlparse(image_url).path))
            content = requests.get(image_url).content
            photo = Photo()
            photo.place = added_place
            photo.image.save(image_filename, ContentFile(content))

    return added_place.title, is_added_place


def get_urls_from_file(path):
    if os.path.exists(path):
        presented_places = 0
        added_places = 0
        with open(path, 'r', encoding='utf-8') as file:
            for url in file.readlines():
                _, added = get_place_from_json(url.strip())
                presented_places += 1
                if added:
                    added_places += 1
    else:
        raise CommandError('File does not exists!')

    return presented_places, added_places
