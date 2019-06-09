"""
Definition of urls for JumpTube.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms
from app import views as app_views
from jump_tube import views


urlpatterns = [
    path('', views.home, name='home'),
#    path('play_video/', views.play_video, name='play_video'),

    path('contact/', app_views.contact, name='contact'),
    path('about/', app_views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
