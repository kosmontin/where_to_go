from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ['num_order', 'image', 'preview']
    readonly_fields = ['preview']
    ordering = ['num_order']

    def preview(self, obj):
        return format_html(
            f'<a href="{obj.image.url}" target="_blank">'
            f'<img src="{obj.image.url}" style="max-height: 200px;"></a>'
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    ordering = ['place', 'num_order']
    fields = ['num_order', 'image', 'preview', 'place']
    readonly_fields = ['preview']

    def preview(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" style="max-height: 200px;"></a>'
        )
