from django import forms
from notes.models import *

from datetime import date 

class NoteForm(forms.Form):
  text = forms.CharField(max_length=1000, widget=forms.Textarea)
  user = forms.CharField(max_length=100)
  def clean(self):
    cleaned_data = super(NoteForm, self).clean()

    return cleaned_data
