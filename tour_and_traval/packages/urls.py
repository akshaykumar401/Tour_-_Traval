from django.urls import path
from . import  views

urlpatterns = [
    path("", views.packages_page , name="packages_page"),
]