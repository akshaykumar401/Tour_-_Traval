from django.db import models
from django.contrib.auth.models import User
# pyrefly: ignore [missing-import]
from packages.models import Packages

# Create your models here.
class Booking(models.Model):
  # Choices for the payment status
  PAYMENT_CHOICES = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed')
  ]

  # Status choices for the booking
  STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
  ]

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  package = models.ForeignKey(Packages, on_delete=models.CASCADE)
  payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES)
  UTR_number = models.CharField(max_length=100, blank=True, null=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  ticket_number = models.CharField(max_length=100, blank=True, null=True)
  number_of_persons = models.IntegerField(default=1)
  start_date = models.DateField()
  end_date = models.DateField()
  total_cost = models.DecimalField(max_digits=10, decimal_places=2)
  
  def __str__(self):
    return f"{self.user} - {self.package} - {self.start_date}"

  
