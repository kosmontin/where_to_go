from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Place


def index(request):
    places = Place.objects.all()
    serialized_places = {"type": "FeatureCollection", "features": []}
    for place in places:
        serialized_places["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(place.lng), float(place.lat)]
            },
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": reverse('place_details', args=(place.pk,))
            }
        })
    return render(request, 'places/index.html', {'places': serialized_places})


def get_place_details(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    serialized_place_details = {
        "title": place.title,
        "imgs": [img.image.url for img in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long
    }
    return JsonResponse(serialized_place_details)
