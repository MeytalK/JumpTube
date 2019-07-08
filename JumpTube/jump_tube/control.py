# -*- coding: utf-8 -*-
"""
This file contain the control services, used for all views
"""

import  pysrt
from jump_tube.models import *
from youtube_transcript_api import YouTubeTranscriptApi
import os
from JumpTube import settings
from django.core.files.storage import FileSystemStorage
import csv


def get_seconds(time):
    return (time.hours * 3600 + time.minutes * 60 + time.seconds + time.milliseconds/1000.0)



def create_video( url = u'',  name = u'', description = u'', srt_file = None, video_file = None, audio_file = None , encoding = 'utf-8', lang = 'iw'):
    
    video = Video( url=url, description = description, name = name, from_file = video_file, audio_file = audio_file)
    video.save()

    video_init_subtitles( video.id, encoding = encoding, language_identifier = lang)

    return video.id



def video_init_subtitles( video_instance_id, encoding = 'utf-8', language_identifier = None):
    try:
        video = Video.objects.get(id=video_instance_id)
    except Video.DoesNotExist:
        return
    
    if language_identifier:
        video.language_identifier = language_identifier
        video.save()

    lang = video.language_identifier
    srt_file = None
    if video.srt_file:
        srt_file = video.srt_file.path        
    else:
        if video.url:
            if  init_subtitles_from_youtube(video.id, languages = [lang]):
                return video.id
            srt_file = get_srt_from_youtube(url = video.url, lang = lang)
        else:
            if video.from_file:
                srt_file = file_mp4_to_srt( video.from_file.path, lang)
            else:
                if video.audio_file:
                    srt_file = file_mp3_to_srt( video.audio_file.path, lang)

    
    print ( 'srt_file', srt_file)
    if srt_file:
        init_subtitles_from_srt_file( srt_file, video.id, encoding = encoding)
        print( 's ' , srt_file, 'v', video.srt_file)
        if not video.srt_file :
            print( 'del of ', srt_file)
            os.system("del " + srt_file + " -y")


                    


    return video.id

def proccess_row(row ):

    movie_id    =  row[ 0] #movie_id
    title	    =  row[ 1] #title	
    category   	=  row[ 2] #category	
    channel	    =  row[ 3] #channel	
    description =  row[ 4] #description
    duration    =  row[ 5] #duration		
    upload_date =  row[ 6] #upload_date	
    channel_id  =  row[ 7] #channel_id

    #print( 'movie_id   ', movie_id   )
    #print( 'title	   ', title	   )
    #print( 'category   ', category   )
    #print( 'channel	   ', channel	   )
    #print( 'description', description)
    #print( 'duration   ', duration   )
    #print( 'upload_date', upload_date)
    if len(movie_id) == 11:
        video_list = Video.objects.filter(url = ('https://www.youtube.com/watch?v=' + movie_id))
        if video_list:
            if video_list[0].subtitle_set.all().count():
                print('skip ', movie_id)
                return True
        subs_from_youtube = get_subtitles_from_youtube(movie_id)
        
        print(movie_id)
        video = Video.objects.get_or_create(url = ('https://www.youtube.com/watch?v=' + movie_id))[0]
        video.name        = title
        video.description = description
        video.save()
        if video.subtitle_set.count():
            return True

        if subs_from_youtube:
            init_with_subtitles_from_youtube( video.id, subs_from_youtube)
        else:
            video_init_subtitles(video.id)
            if video.subtitle_set.count():
                category+= '-RAW_TEXT_TO_SPEECH'
            else:
                video.delete()
                return

        if category:                
            category_instance = Category.objects.get_or_create(name = category)[0]
            category_instance.save()
            video.category = category_instance
        if channel_id:
            channel_instance = YouTubeChannel.objects.get_or_create(channel_id = channel_id)[0]
            channel_instance.name = channel
            channel_instance.save()
            video.youtube_channel = channel_instance

        video.save()
            
        return True    

    return False


def add_videos_from_file( name_of_file_csv, start_from = 0):
    #open csv file
    with_url = 0
    with open(name_of_file_csv, newline='',encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile)
        line_index = 0
        for row in spamreader:
            if line_index > start_from:
                print(line_index)
                if proccess_row(row):
                    with_url +=1
            line_index+=1

    return with_url

def create_video_from_srt_file( name_of_file , url = u'', encoding = 'utf-8', name = u'', description = u'', from_file = None):
    subs = pysrt.open(name_of_file, encoding=encoding)
    video = Video( url=url, description = description, name = name, from_file = from_file)
    video.save()
    
    for s in subs:
        new_sub = video.subtitle_set.create()
        new_sub.text = s.text
        new_sub.index = s.index
        new_sub.starting_in_seconds = get_seconds(s.start)
        new_sub.duration_in_seconds = get_seconds( s.end) - get_seconds(s.start)
        new_sub.save()
        print (new_sub)


def init_subtitles_from_srt_file( name_of_file , video_instance_id = None, encoding = 'utf-8'):
    try:
        video = Video.objects.get(id=video_instance_id)
    except Video.DoesNotExist:
        print( "video not found:" + name_of_file)
        return None

    try:
        subs = pysrt.open(name_of_file, encoding=encoding)
    except TypeError:
        print( "srt file not found")
        return None
    except FileNotFoundError:
        print( "srt file not found")
        return None

    if subs:
        video_delete_all_subtitles(video.id)
        for s in subs:
            new_sub = video.subtitle_set.create()
            new_sub.text = s.text
            new_sub.index = s.index
            new_sub.starting_in_seconds = get_seconds(s.start)
            new_sub.duration_in_seconds = get_seconds( s.end) - get_seconds(s.start)
            new_sub.save()
            print (new_sub)

        return video.id

    return None



def video_delete_all_subtitles(video_instance_id ):
    try:
        video = Video.objects.get(id=video_instance_id)
    except Video.DoesNotExist:
        return

    for subtitle_to_delete in video.subtitle_set.all():
        subtitle_to_delete.delete()


def get_subtitles_from_youtube( video_id, languages =  [ 'iw',  'en', 'ar']):
    try:
        subs_from_youtube = YouTubeTranscriptApi.get_transcript(video_id, languages = languages)
    except YouTubeTranscriptApi.CouldNotRetrieveTranscript:
        return None

    return subs_from_youtube


def init_with_subtitles_from_youtube( video_instance_id, subs_from_youtube = None):
    if None == subs_from_youtube:
        return None


    try:
        video = Video.objects.get(id=video_instance_id)
    except Video.DoesNotExist:
        print( "video not found")
        return None

    if video.url:

        if subs_from_youtube:
            for suntitle_to_delete in video.subtitle_set.all():
                suntitle_to_delete.delete()

            subs_from_youtube_index = 0

            for s in subs_from_youtube:
                new_sub = video.subtitle_set.create()
                new_sub.text = s['text']
                new_sub.index = subs_from_youtube_index
                new_sub.starting_in_seconds = s['start']
                new_sub.duration_in_seconds = s['duration']
                new_sub.save()
                print (new_sub)
                subs_from_youtube_index+=1

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
                new_sub.starting_in_seconds = s['start']
                new_sub.duration_in_seconds = s['duration']
                new_sub.save()
                print (new_sub)
                subs_from_youtube_index+=1

            return video.id

    return None




def get_srt_from_youtube( url, lang = 'iw' ):
    video_id = url[len( 'https://www.youtube.com/watch?v='):]
    file_name = video_id + ".srt"

    os.system("C:\Windows\System32\cmd.exe /c youtube_to_srt.bat " + video_id + " " + lang)

    return file_name



def file_to_srt( mp4_file_name, lang = 'iw' ):
    
    file_name = mp4_file_name + ".srt"

    os.system("C:\Windows\System32\cmd.exe /c file_to_srt.bat " + mp4_file_name + " " + lang)

    return file_name


def file_mp4_to_srt( mp4_file_name, lang = 'iw' ):
    
    file_name = mp4_file_name[:len(mp4_file_name)-len('.mp4')] + ".srt"

    os.system("C:\Windows\System32\cmd.exe /c file_to_srt.bat " + mp4_file_name + " " + lang)

    return file_name



def file_mp3_to_srt( mp3_file_name, lang = 'iw' ):
    
    file_name = mp3_file_name[:len(mp3_file_name)-len('.mp3')] + ".srt"

    os.system("C:\Windows\System32\cmd.exe /c file_to_srt.bat " + mp3_file_name + " " + lang)

    return file_name



def youtube_to_file( url, lang = 'iw' ):
    video_id = url[len( 'https://www.youtube.com/watch?v='):]
    file_name = video_id + ".srt"

    os.system("C:\Windows\System32\cmd.exe /c youtube_to_file.bat " + video_id+ " " + lang)

    return video_id


def youtube_to_file_video( url, lang = 'iw' ):
    video_id = url[len( 'https://www.youtube.com/watch?v='):]
    file_name = video_id + ".srt"

    os.system("C:\Windows\System32\cmd.exe /c youtube_to_file.bat " + video_id+ " " + lang)

    return video_id



def youtube_to_file_audio( url, lang = 'iw' ):
    video_id = url[len( 'https://www.youtube.com/watch?v='):]
    file_name = video_id + ".srt"

    os.system("C:\Windows\System32\cmd.exe /c youtube_to_file.bat " + video_id + " " + lang)

    return video_id



def add_video_from_youtube(url, name = u'', description = u''):
    video = Video.objects.create( url = url)
    video.name = name
    video.description = description
    video.save()

    if init_subtitles_from_youtube(video.id):
        return video.id

    srt_file_name = get_srt_from_youtube(url = url)
    video.srt_file = srt_file_name
    video.save()
    init_subtitles_from_srt_file(settings.MEDIA_ROOT  + '/' + video.srt_file.name, video.id)
    return video.id

def get_subtitles_from_audio_file( audio_file):
    subtitles_file_name = None
    return subtitles_file_name


def get_file_from_youtube( url):
    video_file_name = None
    return video_file_name


def get_subtitles_from_video_file( video_file):
    subtitles_file_name = None
    return subtitles_file_name



#def get_subtitles_file( url= None, video_file = None, audio_file = None):
#    subtitles_file_name = None
#    if url:
#        subtitles_file_name = get_subtitles_from_youtube(url)
#        if subtitles_file_name:
#            return subtitles_file_name
#        video_file_name = get_file_from_youtube(url)
#        if video_file_name:
#            subtitles_file_name = get_subtitles_from_video_file(video_file_name)
#            if subtitles_file_name:
#                return subtitles_file_name
#    return subtitles_file_name