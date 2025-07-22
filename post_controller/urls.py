from django.urls import path
from .views import load_media_by_range

urlpatterns = [
    path('', load_media_by_range, name='load_media_by_range'),
]


