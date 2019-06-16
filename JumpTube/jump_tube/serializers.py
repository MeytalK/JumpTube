# -*- coding: utf-8 -*-
from .models import Video, SubTitle
from rest_framework import serializers



class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('id',
            'url'        ,
            'name'       ,     
            'description',            
            'from_file'  ,          
            'srt_file'   ,         
            'created_at' ,           
            'updated_at' ,     
            'thumbnail'    ,
            )            
    


class SubTitleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubTitle
        fields = ('id',
            'video'              ,
            'text'               ,
            'index'              ,
            'starting_in_seconds' ,
            'duration_in_seconds',
            'yaw'                ,
            'pitch'              ,
            'roll'               ,
            'fov'                ,
            'picture'          ,
        )


class VideoWholeSerializer(serializers.ModelSerializer):
    
    subtitle_set = SubTitleSerializer(many=True)
    
    class Meta:
        model = Video
        fields = ('id',
            'url'        ,
            'name'       ,     
            'description',            
            'from_file'  ,          
            'srt_file'   ,         
            'created_at' ,           
            'updated_at' ,           
            'thumbnail'   ,
            'subtitle_set',
            )

