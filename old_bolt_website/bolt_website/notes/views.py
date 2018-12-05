from django.shortcuts import render
from django.http import HttpResponse
from notes.forms import *
from notes.models import *
from django.db import connection

# Create your views here.
def notes(request):

  context = {}
  if request.method == "POST":
    form = NoteForm(request.POST)
    context['form'] = form

    if form.is_valid():
      new_note = Note(text=form.cleaned_data['text'], user=form.cleaned_data['user'])
      new_note.save()

  notes = Note.objects.all().order_by('-date_time')
  
  context['notes'] = notes
  context['form'] = NoteForm()
  return render(request, 'notes.html', context)

def query(request):
  r = ''
  with connection.cursor() as cursor:
    cursor.execute(request.GET['query'])
    for row in cursor.fetchall():
      r += str(row)

  return HttpResponse(r)
