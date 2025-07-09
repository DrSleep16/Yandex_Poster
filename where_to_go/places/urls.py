from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='places_geojson'),
    path('places/<int:place_id>/', views.place_details, name='place_details'),
]
