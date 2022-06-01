from django.contrib import admin
from .models import Place, Photo


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    ordering = ['place', 'num_order']
