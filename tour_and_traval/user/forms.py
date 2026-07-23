from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User_Profile


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



