# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import ListView, DetailView, CreateView
from .models import SubTitle, Video

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'jump_tube/index.html',
        {
            'video_id':'QqAY0USF9zk',
            'subs':SubTitle.objects.all(),
        }
    )


def video_play(request, pk):
    try:
        video = Video.objects.get(id=int(pk))
    except Video.DoesNotExist:
        return "not found"

    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'jump_tube/index.html',
        {
            'video_id':video.url[len( 'https://www.youtube.com/watch?v='):],
            'subs':video.subtitle_set.all().order_by('stating_in_seconds'),
        }
    )


class VideoListView(ListView):
    """Renders the home page, with a list of all videos."""
    model = Video

class VideoDetailView(DetailView):
    """Renders the poll details page."""
    model = Video

    
class VideoCreateView(CreateView):
    """Renders the poll details page."""
    model = Video


