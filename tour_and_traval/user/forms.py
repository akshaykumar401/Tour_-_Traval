from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# For Authintication Form
class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True)
  full_name = forms.CharField(max_length=100)
  username = forms.CharField(max_length=100)
  phone_number = forms.IntegerField()
  
  class Meta:
    model = User
    fields = ['username', 'email', 'full_name', 'phone_number', 'password1', 'password2']
    
