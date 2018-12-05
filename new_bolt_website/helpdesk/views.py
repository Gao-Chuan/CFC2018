from django.shortcuts import render
from django.http import HttpResponse
from helpdesk.forms import *
from helpdesk.models import *
from django.db import connection
from django.utils.html import escape
from . import models
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from slackclient import SlackClient

def slackbot(msg):
    SLACK_TOKEN = "xoxp-460104746434-461978382534-491854218547-fbe808a868c90b17a782f2e3932e3a9e"
    SLACK_CHANNEL = "#helpdesk"

    sc = SlackClient(SLACK_TOKEN)
    desc = msg
    sc.api_call(
        "chat.postMessage", channel=SLACK_CHANNEL, text=desc,
        username='HelpdeskBot', icon_emoji=':robot_face:'
    )

@login_required
# Create your views here.
def helpdesk(request):

  context = {}
  if request.method == "POST":
    form = HelpdeskForm(request.POST)
    context['form'] = form

    if form.is_valid():
      from_email = settings.EMAIL_HOST_USER
      subject = 'Help from '+form.cleaned_data['user']
      message = form.cleaned_data['question'] + '\n\nFROM:>> ' + form.cleaned_data['email']
      recipient_list = ['dikim33@gmail.com', 'blueteam@ubuntu1604.boltcorp.com', 'iucyberforce2018@gmail.com', 'q7m8z2v2d8i5s7u6@iucfc.slack.com', 'k4z0h0t1l5b6i7f5@iucfc.slack.com', 'r0h0v7i6m1g9p7r3@iucfc.slack.com', 'r1v5f7r1p6y0q0b4@iucfc.slack.com', 'y6i7k3p7o1v2f5z8@iucfc.slack.com']
      send_mail(subject, message ,from_email ,recipient_list , fail_silently=False)
      slackbot('SUBJECT:>>'+ subject + '\n\n' + 'MESSAGE:>>' + message + '\n==============================================')
      # new_help = helpdeskModel(question=form.cleaned_data['question'], user=form.cleaned_data['user'], email=form.cleaned_data['email'])
      # new_help.save()
    return render(request, 'after_sent.html', None)

  context['form'] = HelpdeskForm()
  return render(request, 'helpdesk.html', context)
