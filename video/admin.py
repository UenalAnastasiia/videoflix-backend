from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'created_at', 'video_file')
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title',)

admin.site.register(Video, VideoAdmin)