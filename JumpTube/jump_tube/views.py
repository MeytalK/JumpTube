# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'jump_tube/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
