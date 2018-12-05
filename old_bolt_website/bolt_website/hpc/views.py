from django.shortcuts import render
import netifaces as ni

# Create your views here.
def index(request):
    data = {}

    # Webserver IP = 10.0.x.5
    data['my_ip'] = ni.ifaddresses('eth0')[2][0]['addr']

    # PLC_IP = 10.0.x.200
    hpc_ip = ni.ifaddresses('eth0')[2][0]['addr'].split('.')
    hpc_ip[3] = str(250)
    data['hpc_ip'] = ".".join(hpc_ip)

    return render(request, 'hpc.html', data)

