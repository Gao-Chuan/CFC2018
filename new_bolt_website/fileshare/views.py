from django.shortcuts import render
import netifaces as ni
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def fileshare(request):
    data = {}

    # Webserver IP = 10.0.x.5
    data['my_ip'] = ni.ifaddresses('eth0')[2][0]['addr']

    # PLC_IP = 10.0.x.200
    fileshare_ip = ni.ifaddresses('eth0')[2][0]['addr'].split('.')
    fileshare_ip[3] = str(6)
    data['fileshare_ip'] = ".".join(fileshare_ip)

    return render(request, 'fileshare.html', data)
