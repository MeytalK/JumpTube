from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import *

class VideoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ( 'id','name','description', 'url','language_identifier', 'youtube_channel','category')
#    search_fields  = [ 'id','name','description', 'url','language_identifier', 'youtube_channel','category']
    ordering = ['id']
    pass

class SubTitleAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ( 'id','text','starting_in_seconds')
    ordering = ['id']
    pass

admin.site.register(Video,   VideoAdmin)
admin.site.register(SubTitle, SubTitleAdmin)
admin.site.register(YouTubeChannel)
admin.site.register(Category)

