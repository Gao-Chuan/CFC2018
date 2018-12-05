from django.shortcuts import render
import netifaces as ni

# Create your views here.
def index(request):
    data = {}

    # Webserver IP = 10.0.x.5
    data['my_ip'] = ni.ifaddresses('eth0')[2][0]['addr']

    return render(request, 'hmi.html', data)
