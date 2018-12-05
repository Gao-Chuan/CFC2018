from django.shortcuts import render
from django.http import HttpResponse
from notes.forms import *
from notes.models import *
from django.db import connection
from django.utils.html import escape
from . import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required
@csrf_protect
# Create your views here.
def notes(request):

  context = {}
  if request.method == "POST":
    form = NoteForm(request.POST)
    context['form'] = form

    if form.is_valid():
      new_note = Note(text=form.cleaned_data['text'], user=form.cleaned_data['user'])
      new_note.save()

  notes = models.Note.objects.all().order_by('-date_time')
  
  context['notes'] = notes
  context['form'] = NoteForm()
  return render(request, 'notes.html', context)

@login_required
def query(request):
  doc = """
  If you seen this Doc string it means that you used wrong key word for GET method in your URL.
  You can use: url?query=whatever_you_want_to_search
  Or url?user=whatever_user_you_want_to_search
  """
  context = {}
  r = ''
  if request.GET.get('query'):
    context['notes'] = []
    keyword = request.GET['query']
    with connection.cursor() as cursor:
      query_all = models.Note.objects.filter(Q(text__icontains=keyword)|Q(user__icontains=keyword)|Q(date_time__icontains=keyword))
      for row in query_all:
        context['notes'].append(str(row))
      return render(request, 'api.html', context)

      # cursor.execute(request.GET['query'])
      # for row in cursor.fetchall():
      #   r += str(row)

  elif request.GET.get('user')!= None:
    context['notes'] = []
    keyword = request.GET['user']
    with connection.cursor() as cursor:
      query_user = models.Note.objects.filter(Q(user__icontains=keyword))
      for row in query_user:
        context['notes'].append(str(row))
      return render(request, 'api.html', context)

  else:
    r = doc

  return HttpResponse(r)
