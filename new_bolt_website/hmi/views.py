from django.shortcuts import render
import netifaces as ni
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def index(request):
    data = {}

    # HMI server IP = 10.0.x.15
    data['my_ip'] = ni.ifaddresses('eth0')[2][0]['addr'].split('.')
    data['my_ip'][3] = str(10)
    data['my_ip'] = ".".join(data['my_ip'])

    data['date_ip'] = ni.ifaddresses('eth0')[2][0]['addr']

    return render(request, 'hmi.html', data)
