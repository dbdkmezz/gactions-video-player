from django.contrib import admin

from .models import VideoFolder, Video


admin.site.register(Video)
admin.site.register(VideoFolder)
