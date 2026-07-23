from django.urls import path
from . import  views

urlpatterns = [
    path("reviews/", views.review_page , name="review_page"),
    path("FAQ/", views.FAQ_page , name="FAQ_page"),
]