from django.contrib import admin

from .models import ZoomUsers, ZoomMeetings, ZoomCredentionals

admin.site.register(ZoomUsers)
admin.site.register(ZoomMeetings)
admin.site.register(ZoomCredentionals)