from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('place_details/<int:place_id>/', views.get_place_details),
]
