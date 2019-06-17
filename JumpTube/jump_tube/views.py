# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import SubTitle, Video
from .control import init_subtitles_from_srt_file, init_subtitles_from_youtube
from JumpTube import settings
from django.http import HttpResponse

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    request.user = None
    return video_play(request, "59");
    #return render(
    #    request,
    #    'jump_tube/index.html',
    #    {
    #        'video_id':'QqAY0USF9zk',
    #        'subs':Video.objects.first().subtitle_set.all().order_by('starting_in_seconds'),
    #    }
    #)


def video_play(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        video = Video.objects.first()

    initial_subtitle = None
        
    subtitle  = request.GET.get('subtitle')
    if subtitle:
        try:
            initial_subtitle = video.subtitle_set.all().get(id=int(subtitle))
        except SubTitle.DoesNotExist:
            initial_subtitle = None
         

    if video.from_file:
        return render(
            request,
            'jump_tube/video_view_mp4.html',
           # 'jump_tube/tmp.html',
            {
                'video_id':video.from_file.url,
                'subs':video.subtitle_set.all().order_by('starting_in_seconds'),
                'initial_subtitle':initial_subtitle,
            }
        )

    return render(
        request,
        'jump_tube/index.html',
        {
            'video_id':video.url[len( 'https://www.youtube.com/watch?v='):],
            'subs':video.subtitle_set.all().order_by('starting_in_seconds'),
            'video':video ,
            'initial_subtitle': initial_subtitle,
            'video': video,
        }
    )


def subtitle_play(request, pk):
    try:
        subtitle = SubTitle.objects.get(id=int(pk))
    except SubTitle.DoesNotExist:
        subtitle = SubTitle.objects.first()

  
    #initial_stating_in_seconds  = subtitle.starting_in_seconds

    return HttpResponseRedirect(reverse('video_play', args=(subtitle.video.id,))  + '?subtitle=' +str(subtitle.id))




def video_init_from_srt(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        video = Video.objects.first()
    video_id = None

    if video.srt_file:
        video_id = init_subtitles_from_srt_file( settings.MEDIA_ROOT  + '/' + video.srt_file.name , video.id)
    if None == video_id:
        init_subtitles_from_youtube(video.id)
        

    return HttpResponseRedirect(reverse('video_play', args=(video.id,)))
  
def video_init_from_youtube(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        video = Video.objects.first()

    init_subtitles_from_youtube(video.id)

    return HttpResponseRedirect(reverse('video_play', args=(video.id,)))


def jump(request):
    url_query  = request.GET.get('from_youtube')
    video = Video.objects.get_or_create( url = url_query)[0]
    lang  = request.GET.get('lang')

    print( 'request.GET', request.GET)

    #if lang:
    #    lang_list = []
    #    lang_list.append(lang)
    #    if init_subtitles_from_youtube(video.id, lang_list):
    #        return HttpResponseRedirect(reverse('video_play', args=(video.id,)))

    #    return HttpResponseRedirect(url_query)

    if init_subtitles_from_youtube(video.id):
        return HttpResponseRedirect(reverse('video_play', args=(video.id,)))

    return HttpResponseRedirect(url_query)



def subtitle_set_360_parameters(request, pk):
    try:
        subtitle = SubTitle.objects.get(id=int(pk))
    except SubTitle.DoesNotExist:
        return HttpResponseNotFound("not found - go back")

    if request.GET.get('yaw')    :
        subtitle.yaw    = request.GET.get('yaw')
    if request.GET.get('pitch')  :
        subtitle.pitch  = request.GET.get('pitch')
    if request.GET.get('roll')   :
        subtitle.roll   = request.GET.get('roll')
    if request.GET.get('fov')    :
        subtitle.fov    = request.GET.get('fov')
    subtitle.save()



    #initial_stating_in_seconds  = subtitle.starting_in_seconds

    return HttpResponseRedirect(reverse('video_play', args=(subtitle.video.id,))  + '?subtitle=' +str(subtitle.id))


def video_add_subtitle(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        return HttpResponseNotFound("not found - go back")

    subtitle = video.subtitle_set.create()
    if request.GET.get('starting_in_seconds')    :
        subtitle.starting_in_seconds    = request.GET.get('starting_in_seconds')
    if request.GET.get('yaw')    :
        subtitle.yaw    = request.GET.get('yaw')
    if request.GET.get('pitch')  :
        subtitle.pitch  = request.GET.get('pitch')
    if request.GET.get('roll')   :
        subtitle.roll   = request.GET.get('roll')
    if request.GET.get('fov')    :
        subtitle.fov    = request.GET.get('fov')
    subtitle.save()

    return HttpResponseRedirect("/admin/jump_tube/subtitle/"+str(subtitle.id)+ "/change/")
        

def jump_to_language(request, language):
    url_query  = request.GET.get('from_youtube')
    video = Video.objects.get_or_create( url = url_query)[0]
    
    language_list = []
    language_list.append(language)

    if init_subtitles_from_youtube(video.id, language = language_list):
        return HttpResponseRedirect(reverse('video_play', args=(video.id,)))
    return HttpResponseRedirect(url_query)



class VideoListView(ListView):
    """Renders the home page, with a list of all videos."""
    model = Video

class VideoDetailView(DetailView):
    """Renders the poll details page."""
    model = Video

    
class VideoCreateView(CreateView):
    """Renders the poll details page."""
    model = Video


