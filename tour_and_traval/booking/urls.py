from django.urls import path
from .import views

urlpatterns = [
  path("payment/<int:package_id>/<str:start_date>/<str:persons>/", views.payment_page, name="payment_page"),
  path("payment/success/<int:booking_id>/<str:payment_id>/<str:transection_id>/<int:package_id>/", views.booking_success_page, name="booking_success_page"),
  path("payment/verify/", views.payment_verify, name="payment_verify"),
  path("cancel/<int:booking_id>/", views.cancel_pending_booking, name="cancel_pending_booking"),
]