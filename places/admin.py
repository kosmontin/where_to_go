from django.contrib import admin
from .models import Place, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    ordering = ['num_order']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    ordering = ['place', 'num_order']
