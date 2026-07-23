from django.urls import path
from .import views

urlpatterns = [
  path("payment/<slug:slug>/<str:start_date>/<str:persons>/", views.payment_page, name="payment_page"),
  path("payment/success/<slug:booking_id>/<str:payment_id>/<str:transection_id>/<slug:package_id>/", views.booking_success_page, name="booking_success_page"),
  path("payment/verify/", views.payment_verify, name="payment_verify"),
  path("cancel/<slug:booking_id>/", views.cancel_pending_booking, name="cancel_pending_booking"),
]