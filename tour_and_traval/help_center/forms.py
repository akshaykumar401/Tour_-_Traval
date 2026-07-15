from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
  class Meta:
    model = Feedback
    fields = ['full_name', 'email', 'message', 'reating']

class AIAgentForm(forms.Form):
  query = forms.CharField(max_length=500, strip=True)
