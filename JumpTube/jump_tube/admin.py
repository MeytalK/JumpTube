from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import *

admin.site.register(Video)
admin.site.register(SubTitle)

