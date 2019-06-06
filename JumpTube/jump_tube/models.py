from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
MAX_TEXT = 2000

class Video(models.Model):
#    owner                       = models.ForeignKey(User, on_delete=models.CASCADE)
    url                         = models.URLField( default=None, blank=True, null=True)                                                   
    offset_seconds              = models.FloatField(default=0.0)
    name                        = models.TextField(default = u'', blank=True, null=True, max_length = MAX_TEXT)
    description                 = models.TextField( blank=True, null=True,max_length = MAX_TEXT)
    created_at                  = models.DateTimeField(auto_now_add=True)
    updated_at                  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ' ' + self.name


class SubTitle(models.Model):
    video                       = models.ForeignKey(Video, on_delete=models.CASCADE)
    text                        = models.TextField(default = u'', blank=True, null=True, max_length = MAX_TEXT)
    index                       = models.IntegerField(default = 0)
    stating_in_seconds          = models.FloatField(default   = 0.0)
    duration_in_seconds         = models.FloatField(default   = 0.0)
    def __str__(self):
        return str(self.index) + ' ' + self.text


