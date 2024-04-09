from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'creator']
    list_display = ['id', 'name', 'creator']


admin.site.register(Category, CategoryAdmin)