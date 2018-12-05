from django.urls import path

from . import views

urlpatterns = [
  path('', views.inventory_tracker, name='inventory_tracker'),
]
