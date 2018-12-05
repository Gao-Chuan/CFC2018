from django import forms
from helpdesk.models import *

from datetime import date 

class HelpdeskForm(forms.Form):
  user = forms.CharField(max_length=100)
  email = forms.CharField(max_length=100)
  question = forms.CharField(max_length=1000, widget=forms.Textarea)
  def clean(self):
    cleaned_data = super(HelpdeskForm, self).clean()

    return cleaned_data
