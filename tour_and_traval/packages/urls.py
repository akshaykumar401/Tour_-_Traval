from django.urls import path
from . import  views

urlpatterns = [
    path("", views.packages_page , name="packages_page"),
    path("package_detail/<int:packages_id>/", views.packages_detail_page , name="packages_detail_page"),
]