# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import SubTitle, Video
from .control import init_subtitles_from_srt_file, init_subtitles_from_youtube, get_srt_from_youtube, video_init_subtitles
from JumpTube import settings
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return HttpResponseRedirect(reverse('video_list'))
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

@login_required
def video_play(request, pk):
    #if not request.user.is_authenticated:
    #    print( 'request.path', request.path)
    #    return redirect('/accounts/login/?next_page=' +  request.path)

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
            'jump_tube/video_play.html',
           # 'jump_tube/tmp.html',
            {
            'page_name':video.name,
            'subs':video.subtitle_set.all().order_by('starting_in_seconds'),
            'video':video ,
            'initial_subtitle': initial_subtitle,
            }
        )

    if video.audio_file:
        return render(
        request,
        'jump_tube/audio_play.html',
        {
            'page_name':video.name,
            'subs':video.subtitle_set.all().order_by('starting_in_seconds'),
            'video':video ,
            'initial_subtitle': initial_subtitle,
        }
    )


    return render(
        request,
        #'jump_tube/index.html',
        'jump_tube/youtube_play.html',
        {
            'page_name':video.name,
            'video_id':video.url[len( 'https://www.youtube.com/watch?v='):],
            'subs':video.subtitle_set.all().order_by('starting_in_seconds'),
            'video':video ,
            'initial_subtitle': initial_subtitle,
        }
    )


def subtitle_play(request, pk):
    try:
        subtitle = SubTitle.objects.get(id=int(pk))
    except SubTitle.DoesNotExist:
        subtitle = SubTitle.objects.first()

  
    #initial_stating_in_seconds  = subtitle.starting_in_seconds

    return HttpResponseRedirect(reverse('video_play', args=(subtitle.video.id,))  + '?subtitle=' +str(subtitle.id))



@login_required
def video_delete_all_subtitles(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        return HttpResponseNotFound("not found - go back")

    for subtitle_to_delete in video.subtitle_set.all():
                subtitle_to_delete.delete()

    return HttpResponseRedirect(reverse('video_play', args=(video.id,)))

@login_required
def video_init_from_srt(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        return HttpResponseNotFound("not found - go back")

    video_init_subtitles(video.id)
        

    return HttpResponseRedirect(reverse('video_play', args=(video.id,)))
  
@login_required
def video_init_from_youtube(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        return HttpResponseNotFound("not found - go back")

    init_subtitles_from_youtube(video.id)

    return HttpResponseRedirect(reverse('video_play', args=(video.id,)))

@login_required
def jump(request):
    print( 'request.GET', request.GET)
    print( 'request.GET', request.GET.get('v'))
    print( 'request.GET', request.GET.get('from_youtube'))
    if request.GET.get('v'):
        url_query = "https://www.youtube.com/watch?v=" + request.GET.get('v')
        print('resolved', url_query)
    else:
        url_query = request.GET.get('from_youtube')

    
   
    #url_query  = request.GET.get('from_youtube')
    #video = Video.objects.get_or_create( url = url_query)[0]


    video = Video.objects.create( url = url_query)
    video.save()
    lang  = request.GET.get('lang')

    print( 'request.GET', request.GET)
    

    #if lang:
    #    lang_list = []
    #    lang_list.append(lang)
    #    if init_subtitles_from_youtube(video.id, lang_list):
    #        return HttpResponseRedirect(reverse('video_play', args=(video.id,)))

    #    return HttpResponseRedirect(url_query)

    video_init_subtitles((video.id), language_identifier=lang)
    #if init_subtitles_from_youtube(video.id):
    #    return HttpResponseRedirect(reverse('video_play', args=(video.id,)))

    #srt_file_name = get_srt_from_youtube(url = url_query)
    #print(srt_file_name)
    #video.srt_file = srt_file_name
    #video.save()
    #init_subtitles_from_srt_file( video.srt_file.name, video.id)
    return HttpResponseRedirect(reverse('video_play', args=(video.id,)))
    

#    return HttpResponseRedirect(url_query)


@login_required
def subtitle_set_360_parameters(request, pk):
    try:
        subtitle = SubTitle.objects.get(id=int(pk))
    except SubTitle.DoesNotExist:
        return HttpResponseNotFound("not found - go back")
    print(request.GET)
    if request.GET.get('yaw')    :
        subtitle.yaw    = request.GET.get('yaw')
    if request.GET.get('pitch')  :
        subtitle.pitch  = request.GET.get('pitch')
    if request.GET.get('roll')   :
        subtitle.roll   = request.GET.get('roll')
    if request.GET.get('fov')    :
        subtitle.fov    = request.GET.get('fov')
    subtitle.save()
    print(subtitle)


    #initial_stating_in_seconds  = subtitle.starting_in_seconds

    return HttpResponseRedirect(reverse('video_play', args=(subtitle.video.id,))  + '?subtitle=' +str(subtitle.id))

@login_required
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


    
class VideoUpdateView(UpdateView):
    """Renders the poll details page."""
    model = Video

    
class SubTitleDetailView(DetailView):
    """Renders the poll details page."""
    model = SubTitle

    

    
class SubTitleUpdateView(UpdateView):
    """Renders the poll details page."""
    model = SubTitle

