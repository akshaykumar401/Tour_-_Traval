from django import forms

class SearchPackageForm(forms.Form):
  location = forms.CharField(max_length=100, required=True, label="Where to next?")
  date = forms.DateField(required=True, label="When are you travel?")
  
  class Meta:
    fields = ['location', 'date']