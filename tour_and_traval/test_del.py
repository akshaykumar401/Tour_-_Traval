import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour_and_traval.settings')
django.setup()

from django.test import Client
from booking.models import Booking
from django.contrib.auth.models import User

user, _ = User.objects.get_or_create(username='admin2', is_superuser=True, is_staff=True)
user.set_password('123')
user.save()

client = Client()
client.login(username='admin2', password='123')
b = Booking.objects.first()
if b:
    res = client.post(f'/admin/booking/booking/{b.pk}/delete/', data={'post': 'yes'})
    print(res.status_code)
