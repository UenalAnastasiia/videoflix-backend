from django.contrib import admin
from .models import Video
from import_export.admin import ImportExportModelAdmin


class VideoAdmin(ImportExportModelAdmin):
    fields = ('title', 'description', 'created_at', 'video_file', 'creator', 'cover_picture', 'category', 'release_year', 'age')
    list_display = ('id', 'title', 'created_at', 'creator')
    search_fields = ('title', 'category',)

admin.site.register(Video, VideoAdmin)
