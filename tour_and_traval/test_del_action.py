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

# Need a fresh booking to delete
user = User.objects.get(username='admin3')
# Let's create a dummy booking
from packages.models import Packages
from datetime import date
pkg = Packages.objects.first()
if not pkg:
    pkg = Packages.objects.create(mini_title='test', main_title='test', starting_price=100, total_days=1, total_nights=1, max_people=2, category='Beach', location='Beach')
b = Booking.objects.create(user=user, package=pkg, payment_status='paid', status='confirmed', amount=100, total_cost=100, start_date=date.today(), end_date=date.today())

client = Client()
client.login(username='admin3', password='123')

# test delete selected action
# First GET to confirmation page
data = {
    'action': 'delete_selected',
    '_selected_action': [str(b.pk)]
}
res = client.post('/admin/booking/booking/', data=data)
print("Action selection STATUS:", res.status_code)
if res.status_code == 200:
    # POST to confirm deletion
    data['post'] = 'yes'
    res2 = client.post('/admin/booking/booking/', data=data)
    print("Action confirm STATUS:", res2.status_code)
    if res2.status_code == 500:
        with open('error_action.html', 'wb') as f:
            f.write(res2.content)
            print("Error written to error_action.html")
