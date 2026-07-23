from django.urls import path
from . import  views

urlpatterns = [
    path("", views.gallery_page , name="gallery_page"),
]