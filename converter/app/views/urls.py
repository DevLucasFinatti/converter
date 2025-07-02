from django.urls import path
from .image import img_convert
from .video import video_convert

urlpatterns = [
    path('api/convert-image/', img_convert, name='convert-image-api'),
    path('api/convert-video/', video_convert, name='convert-video-api'),
]