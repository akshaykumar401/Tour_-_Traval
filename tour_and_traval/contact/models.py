from django.db import models

# Create your models here.
class Contact(models.Model):
  # Subject ENUM
  SUBJECT_CHOICES = [
    ('General Inquiry', 'General Inquiry'),
    ('Booking Questions', 'Booking Questions'),
    ('Payment Issues', 'Payment Issues'),
    ('Custom Itinerary Request', 'Custom Itinerary Request'),
    ('Feedback', 'Feedback'),
    ('Partnership Opportunities', 'Partnership Opportunities'),
    ('Other', 'Other'),
  ]
  
  full_name = models.CharField(max_length=50, help_text="Enter your full name")
  email = models.EmailField(max_length=50, help_text="Enter your email address")
  subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES, help_text="Select the subject of your inquiry")
  message = models.TextField(max_length=500, help_text="Enter your message")
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.full_name
