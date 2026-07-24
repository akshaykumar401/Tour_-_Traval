import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour_and_traval.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS = ['*']

from django.test import Client
from booking.models import Booking
from django.contrib.auth.models import User
import traceback

user, _ = User.objects.get_or_create(username='admin3', is_superuser=True, is_staff=True)
user.set_password('123')
user.save()

client = Client()
client.login(username='admin3', password='123')

# test delete view
b = Booking.objects.first()
if b:
    print(f"Trying to delete booking {b.pk}")
    res = client.post(f'/admin/booking/booking/{b.pk}/delete/', data={'post': 'yes'})
    print("STATUS:", res.status_code)
    if res.status_code == 500:
        with open('error.html', 'wb') as f:
            f.write(res.content)
        print("Error written to error.html")
else:
    print("No bookings to delete")
