from django.contrib import admin 
from imagekit.admin import AdminThumbnail
from .models import *

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'modified','thumbnail',]

    photo_thumbnail = AdminThumbnail(image_field='photo_thumbnail')
    list_filter = ["user","created"]
    search_fields = ["user","created"]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['mobile_no', 'imei',]
    list_filter = ['mobile_no', 'imei',]
    search_fields = ['mobile_no', 'imei',]


class ThingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value',]
    list_filter = ['key', 'value',]
    search_fields = ['key', 'value',]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Thing, ThingAdmin)