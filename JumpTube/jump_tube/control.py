# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

import  pysrt
from jump_tube.models import *


def get_seconds(time):
    return (time.hours * 3600 + time.minutes * 60 + time.seconds + time.milliseconds/1000.0)



def create_video_from_srt_file( name_of_file , url = u'', encoding = 'utf-8', name = u'', description = u'', from_file = None):
    subs = pysrt.open(name_of_file, encoding=encoding)
    video = Video( url=url, description = description, name = name, from_file = from_file)
    video.save()
    
    for s in subs:
        new_sub = video.subtitle_set.create()
        new_sub.text = s.text
        new_sub.index = s.index
        new_sub.stating_in_seconds = get_seconds(s.start)
        new_sub.duration_in_seconds = get_seconds( s.end) - get_seconds(s.start)
        new_sub.save()
        print (new_sub)


def init_subtitles_from_srt_file( name_of_file , video_instance_id , encoding = 'utf-8'):
    try:
        video = Video.objects.get(id=video_instance_id)
    except Video.DoesNotExist:
        print( "video not found")
        return None

    for suntitle_to_delete in video.subtitle_set.all():
        suntitle_to_delete.delete()

    subs = pysrt.open(name_of_file, encoding=encoding)
    
    for s in subs:
        new_sub = video.subtitle_set.create()
        new_sub.text = s.text
        new_sub.index = s.index
        new_sub.stating_in_seconds = get_seconds(s.start)
        new_sub.duration_in_seconds = get_seconds( s.end) - get_seconds(s.start)
        new_sub.save()
        print (new_sub)


