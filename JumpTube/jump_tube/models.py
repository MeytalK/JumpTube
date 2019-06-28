from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
MAX_TEXT = 2000

class Video(models.Model):
    url                 = models.URLField( default=None, blank=True, null=True)                                                   
    name                = models.TextField(default = u'', blank=True, null=True, max_length = MAX_TEXT)
    description         = models.TextField( default = u'',blank=True, null=True,max_length = MAX_TEXT)
    from_file           = models.FileField(default = None, blank=True, null=True,upload_to='uploads/%Y/%m/%d/', max_length = 100000000000)
    srt_file            = models.FileField(default = None, blank=True, null=True,upload_to='uploads/%Y/%m/%d/', max_length = 100000000)
    audio_file          = models.FileField(default = None, blank=True, null=True,upload_to='uploads/%Y/%m/%d/', max_length = 100000000000)
    thumbnail           = models.ImageField(default = None, blank=True, null=True,upload_to='uploads/%Y/%m/%d/', max_length = 100000000)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    starting_in_seconds = models.FloatField(default   = 0.0)
    yaw                 = models.FloatField(default   = 0.0  )
    pitch               = models.FloatField(default   = 0.0  )
    roll                = models.FloatField(default   = 0.0  )
    fov                 = models.FloatField(default   = 100.0)
    language_identifier = models.CharField( default = u'iw',max_length = 100)
    

    def __str__(self):
        if self.url:
            return str(self.id) + ' ' + self.name + ' ' + self.url 
        return str(self.id) + ' ' + self.name
    
    def get_absolute_url(self):
        return (
            reverse('video_play', kwargs={'pk': str(self.id)}) )

        #return self.video.url + '&t=' + str(int(self.starting_in_seconds)) + 's'

class SubTitle(models.Model):
    video              = models.ForeignKey(Video, on_delete=models.CASCADE)
    text               = models.TextField(default = u'', blank=True, null=True, max_length = MAX_TEXT)
    index              = models.IntegerField(default = 0)
    starting_in_seconds= models.FloatField(default   = 0.0)
    duration_in_seconds= models.FloatField(default   = 0.0)
    picture            = models.ImageField(default = None, blank=True, null=True,upload_to='uploads/%Y/%m/%d/', max_length = 100000000)
    yaw                = models.FloatField(default   = 0.0  )
    pitch              = models.FloatField(default   = 0.0  )
    roll               = models.FloatField(default   = 0.0  )
    fov                = models.FloatField(default   = 100.0  )
    def __str__(self):
        return str(self.index) + ' ' + self.text


    
    def get_absolute_url(self):


        return (
            reverse('subtitle_play', kwargs={'pk': str(self.id)}) 
                    )
