# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

import  pysrt
from jump_tube.models import *
from youtube_transcript_api import YouTubeTranscriptApi


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


    subs = pysrt.open(name_of_file, encoding=encoding)
    if subs:
        for suntitle_to_delete in video.subtitle_set.all():
            suntitle_to_delete.delete()
   
        for s in subs:
            new_sub = video.subtitle_set.create()
            new_sub.text = s.text
            new_sub.index = s.index
            new_sub.stating_in_seconds = get_seconds(s.start)
            new_sub.duration_in_seconds = get_seconds( s.end) - get_seconds(s.start)
            new_sub.save()
            print (new_sub)
            return video.id

    return None


def init_subtitles_from_youtube( video_instance_id, languages =  [ 'iw',  'en', 'ar']):
    try:
        video = Video.objects.get(id=video_instance_id)
    except Video.DoesNotExist:
        print( "video not found")
        return None

    if video.url:
        try:
            subs_from_youtube = YouTubeTranscriptApi.get_transcript(video.url[len( 'https://www.youtube.com/watch?v='):], languages = languages)
        except YouTubeTranscriptApi.CouldNotRetrieveTranscript:
            return None

        if subs_from_youtube:
            for suntitle_to_delete in video.subtitle_set.all():
                suntitle_to_delete.delete()

            subs_from_youtube_index = 0

            for s in subs_from_youtube:
                new_sub = video.subtitle_set.create()
                new_sub.text = s['text']
                new_sub.index = subs_from_youtube_index
                new_sub.stating_in_seconds = s['start']
                new_sub.duration_in_seconds = s['duration']
                new_sub.save()
                print (new_sub)
                subs_from_youtube_index+=1

            return video.id

    return None


