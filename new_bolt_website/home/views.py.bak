from django.shortcuts import render
import netifaces as ni

# Create your views here.
def index(request):
    data = {}

    # Webserver IP = 10.0.x.5
    data['my_ip'] = ni.ifaddresses('eth0')[2][0]['addr']

    # PLC_IP = 10.0.x.200
    plc_ip = ni.ifaddresses('eth0')[2][0]['addr'].split('.')
    plc_ip[3] = str(200)
    data['plc_ip'] = ".".join(plc_ip)

    return render(request, 'index.html', data)

