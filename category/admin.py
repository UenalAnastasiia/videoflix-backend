from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'creator', 'content']
    list_display = ['id', 'name', 'creator', 'content']


admin.site.register(Category, CategoryAdmin)
