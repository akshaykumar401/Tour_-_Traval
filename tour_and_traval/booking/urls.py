from django.urls import path
from .import views

urlpatterns = [
  path("", views.booking_page, name="booking_page"),
  path("payment/<int:package_id>/", views.payment_page, name="payment_page"),
  path("payment/success/<int:booking_id>/<int:payment_id>/<str:transection_id>/<int:package_id>/", views.booking_success_page, name="booking_success_page"),
]