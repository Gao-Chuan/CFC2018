from django.urls import path

from . import views

urlpatterns = [
  path('', views.notes, name='notes'),
  path('api/v1/query', views.query, name='query'),
]
