import os.path
from urllib.parse import unquote, urlparse
from urllib.request import urlretrieve

import requests
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError
from places.models import Photo, Place
from where_to_go import settings


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
    place_json = response.json()
    added_place, is_added_place = Place.objects.get_or_create(
        title=place_json['title'],
        description_short=place_json['description_short'],
        description_long=place_json['description_long'],
        lng=place_json['coordinates']['lng'],
        lat=place_json['coordinates']['lat']
    )
    if is_added_place:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'tmp'), exist_ok=True)
        for image_url in place_json['imgs']:
            image_filename = os.path.basename(
                unquote(urlparse(image_url).path))
            image_path = os.path.join(
                settings.MEDIA_ROOT, 'tmp', image_filename)
            urlretrieve(image_url, image_path)

            photo = Photo()
            photo.place = added_place
            with open(image_path, 'rb') as dl_file:
                photo.image.save(image_filename, ImageFile(dl_file))
            os.remove(image_path)

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
