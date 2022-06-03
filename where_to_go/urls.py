from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('', include('places.urls')),
]
