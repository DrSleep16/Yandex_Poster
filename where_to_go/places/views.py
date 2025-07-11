from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Place, PlaceImage


def main_page(request):
    features = []
    for place in Place.objects.all():
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lng, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                "detailsUrl": reverse('place_details', args=[place.id]),
            }
        })
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    return render(request, 'index.html', {'geojson': geojson})


def place_details(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    images = PlaceImage.objects.filter(place=place).order_by('order')
    imgs = [img.image.url for img in images]

    data = {
        'title': place.title,
        'imgs': imgs,
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lat': place.lat,
            'lng': place.lng,
        }
    }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})


def place_title(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    return HttpResponse(place.title)
