# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

import  pysrt
from .models import *


def get_seconds(srt_item):
    return (srt_item.start.hours * 3600 + srt_item.start.minutes * 60 + srt_item.start.seconds)


def create_video_from_srt_file( name_of_file , url = u'', encoding = 'utf-8'):
    subs = pysrt.open(name_of_file, encoding=encoding)
    video = Video( url='https://www.youtube.com/watch?v=QqAY0USF9zk')
    video.save()

    for s in subs:
        new_sub = video.subtitle_set.create()
        new_sub.text = s.text
        new_sub.index = s.index
        new_sub.stating_in_seconds = float(get_seconds(s))
        new_sub.save()
        print (str(get_seconds(s)) + ' '+ s.text)
  
