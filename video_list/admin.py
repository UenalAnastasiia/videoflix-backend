from django.contrib import admin
from .models import List


class ListAdmin(admin.ModelAdmin):
    fields = ['creator', 'list']
    list_display = ['id', 'creator']


admin.site.register(List, ListAdmin)