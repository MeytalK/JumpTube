# -*- coding: utf-8 -*-
from rest_framework import viewsets
from .serializers import VideoSerializer, SubTitleSerializer, VideoWholeSerializer
from .models import Video, SubTitle
from rest_framework.views import APIView
from rest_framework.response import Response

class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Video.objects.all().order_by('id')
    serializer_class = VideoSerializer


class SubTitleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SubTitle.objects.all()
    serializer_class = SubTitleSerializer




class VideoWholeView(APIView):
    def get_object(self, pk):
            try:
                return Video.objects.get(pk = pk)
            except Video.DoesNotExist:
                raise Http404
            
    def get(self, request, pk, format = None):
        video = self.get_object(pk)
        serializer_context = {
            'request': request,
        }

                
        serialized_video = VideoWholeSerializer(video, context=serializer_context)
        return Response(serialized_video.data)
