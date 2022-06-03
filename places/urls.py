from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('place_details/<int:place_id>/', views.get_place_details),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
