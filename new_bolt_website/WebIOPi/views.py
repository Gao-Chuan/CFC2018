from django.shortcuts import render
import netifaces as ni
from django.contrib.auth.decorators import login_required

@login_required
# Create your views here.
def WebIOPi(request):
    data = {}

    # Webserver IP = 10.0.x.5
    data['my_ip'] = ni.ifaddresses('eth0')[2][0]['addr']

    # PLC_IP = 10.0.x.200
    plc_ip = ni.ifaddresses('eth0')[2][0]['addr'].split('.')
    plc_ip[3] = str(200)
    data['plc_ip'] = ".".join(plc_ip)
    return render(request, 'WebIOPi.html', data)