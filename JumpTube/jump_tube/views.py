# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import SubTitle

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


