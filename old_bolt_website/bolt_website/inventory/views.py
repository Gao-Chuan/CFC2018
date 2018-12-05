from django.shortcuts import render
from django.http import HttpResponse
import netifaces as ni

# Create your views here.
def inventory_tracker(request):

  context = {}
  context['my_ip'] = ni.ifaddresses('eth0')[2][0]['addr']
  return render(request, 'inventory.html', context)

