from django.urls import path

from . import views

urlpatterns = [
  path('', views.WebIOPi, name='WebIOPi'),
]
