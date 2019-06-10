"""
Definition of urls for polls viewing and voting.
"""

from django.urls import path
from jump_tube.models import Video, SubTitle
import jump_tube.views

urlpatterns = [
    path('video_list/',
        jump_tube.views.VideoListView.as_view(
            queryset=Video.objects.order_by('-created_at'),
            context_object_name='video_list',
            template_name='jump_tube/video_list.html',),
        name='video_list'),
    path('video_create/',
        jump_tube.views.VideoListView.as_view(
            template_name='jump_tube/video_create.html',),
        name='video_create'),
    path('<int:pk>/',
        jump_tube.views.VideoDetailView.as_view(
            template_name='jump_tube/details.html'),
        name='detail'),
]
