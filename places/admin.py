from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from .models import Place, Photo


class PhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Photo
    fields = ['num_order', 'image', 'preview']
    readonly_fields = ['preview']

    def preview(self, obj):
        image_url = obj.image.url
        return format_html(
            f'<a href="{image_url}" target="_blank">'
            f'<img src="{image_url}" style="max-height: 200px;"></a>'
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ['title']
    inlines = [PhotoInline]
