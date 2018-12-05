from django.db import models
import datetime

# Create your models here.
class Note(models.Model):

  text = models.CharField(max_length=1000)

  user = models.CharField(max_length=100)

  date_time = models.DateTimeField(default=datetime.datetime.now)

  def __unicode__(self):
    return self.text + ' by: ' + self.user + ' at: ' + str(self.date_time)

  def __repr__(self):
    return self.text + ' by: ' + self.user + ' at: ' + str(self.date_time)

  def __str__(self):
    return self.text + ' by: ' + self.user + ' at: ' + str(self.date_time)
