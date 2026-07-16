from django.contrib import admin
from .models import Booking

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'package', 'payment_status', 'status', 'UTR_number', 'amount', 'updated_at', 'created_at', 'ticket_number', 'number_of_persons', 'start_date', 'end_date', 'total_cost')
  list_filter = ('user', 'package', 'payment_status', 'status', 'updated_at', 'created_at', 'start_date', 'end_date')
