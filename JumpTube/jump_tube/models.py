from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
MAX_TEXT = 2000

    #LANGUAGE_CODES = 
    #    'af': 'Afrikaans',
    #    'ar': 'Arabic',
    #    'az': 'Azerbaijani',
    #    'be': 'Belarusian',
    #    'bg': 'Bulgarian',
    #    'bn': 'Bengali',
    #    'bs': 'Bosnian',
    #    'ca': 'Catalan',
    #    'ceb': 'Cebuano',
    #    'cs': 'Czech',
    #    'cy': 'Welsh',
    #    'da': 'Danish',
    #    'de': 'German',
    #    'el': 'Greek',
    #    'en': 'English',
    #    'eo': 'Esperanto',
    #    'es': 'Spanish',
    #    'et': 'Estonian',
    #    'eu': 'Basque',
    #    'fa': 'Persian',
    #    'fi': 'Finnish',
    #    'fr': 'French',
    #    'ga': 'Irish',
    #    'gl': 'Galician',
    #    'gu': 'Gujarati',
    #    'ha': 'Hausa',
    #    'hi': 'Hindi',
    #    'hmn': 'Hmong',
    #    'hr': 'Croatian',
    #    'ht': 'Haitian Creole',
    #    'hu': 'Hungarian',
    #    'hy': 'Armenian',
    #    'id': 'Indonesian',
    #    'ig': 'Igbo',
    #    'is': 'Icelandic',
    #    'it': 'Italian',
    #    'iw': 'Hebrew',
    #    'ja': 'Japanese',
    #    'jw': 'Javanese',
    #    'ka': 'Georgian',
    #    'kk': 'Kazakh',
    #    'km': 'Khmer',
    #    'kn': 'Kannada',
    #    'ko': 'Korean',
    #    'la': 'Latin',
    #    'lo': 'Lao',
    #    'lt': 'Lithuanian',
    #    'lv': 'Latvian',
    #    'mg': 'Malagasy',
    #    'mi': 'Maori',
    #    'mk': 'Macedonian',
    #    'ml': 'Malayalam',
    #    'mn': 'Mongolian',
    #    'mr': 'Marathi',
    #    'ms': 'Malay',
    #    'mt': 'Maltese',
    #    'my': 'Myanmar (Burmese)',
    #    'ne': 'Nepali',
    #    'nl': 'Dutch',
    #    'no': 'Norwegian',
    #    'ny': 'Chichewa',
    #    'pa': 'Punjabi',
    #    'pl': 'Polish',
    #    'pt': 'Portuguese',
    #    'ro': 'Romanian',
    #    'ru': 'Russian',
    #    'si': 'Sinhala',
    #    'sk': 'Slovak',
    #    'sl': 'Slovenian',
    #    'so': 'Somali',
    #    'sq': 'Albanian',
    #    'sr': 'Serbian',
    #    'st': 'Sesotho',
    #    'su': 'Sudanese',
    #    'sv': 'Swedish',
    #    'sw': 'Swahili',
    #    'ta': 'Tamil',
    #    'te': 'Telugu',
    #    'tg': 'Tajik',
    #    'th': 'Thai',
    #    'tl': 'Filipino',
    #    'tr': 'Turkish',
    #    'uk': 'Ukrainian',
    #    'ur': 'Urdu',
    #    'uz': 'Uzbek',
    #    'vi': 'Vietnamese',
    #    'yi': 'Yiddish',
    #    'yo': 'Yoruba',
    #    'zh-CN': 'Chinese (Simplified)',
    #    'zh-TW': 'Chinese (Traditional)',
    #    'zu': 'Zulu',
    #}


class Category(models.Model):    
    name                = models.TextField(default = u'', blank=True, null=True, max_length = MAX_TEXT)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class YouTubeChannel(models.Model):    
    channel_id          = models.TextField(default = u'', blank=True, null=True,  max_length = 24)                                                   
    name                = models.TextField(default = u'', blank=True, null=True, max_length = MAX_TEXT)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


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
    youtube_channel     = models.ForeignKey(YouTubeChannel, on_delete = models.SET_NULL, null=True, blank=True)
    category            = models.ForeignKey(Category, on_delete = models.SET_NULL, null=True, blank=True)
    #language            = models.CharField( choices)
    

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
