from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.template import loader
import logging
import requests

from .models import User_Profile


from django.conf import settings
logger = logging.getLogger(__name__)
MAIL_SERVICE_URL = settings.MAIL_SERVICE_URL

class MailServicePasswordResetForm(PasswordResetForm):
  def send_mail(
    self,
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name=None,
  ):
    subject = ''.join(loader.render_to_string(subject_template_name, context).splitlines())
    body = loader.render_to_string(email_template_name, context)

    try:
      response = requests.post(
        MAIL_SERVICE_URL,
        json={
          'recipients': to_email,
          'subject': subject,
          'body': body,
        },
        timeout=10,
      )
      response.raise_for_status()
    except requests.RequestException:
      logger.exception('Failed to send password reset email to %s', context['user'].pk)


# For Authintication Form
class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True)
  full_name = forms.CharField(max_length=100)
  username = forms.CharField(max_length=100)
  phone_number = forms.IntegerField()
  
  class Meta:
    model = User
    fields = ['username', 'email', 'full_name', 'phone_number', 'password1', 'password2']

class UserProfileForm(forms.Form):
  full_name = forms.CharField(max_length=100, required=True, label='Full Name')
  phone_number = forms.IntegerField()
  address = forms.CharField(max_length=255)
  
  class Meta:
    model = User_Profile
    fields = ['full_name', 'phone_number', 'address']

class UpdateUserProfilePhotoForm(forms.Form):
  image = forms.ImageField(required=True, label='Profile Photo')


