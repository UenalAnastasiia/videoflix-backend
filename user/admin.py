from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets, 
        (
            'Individuelle Daten',
            {
                'fields': (
                    'custom',
                    'phone',
                    'street',
                    'city',
                    'image',
                    'email_confirmation_token',
                    'email_confirmed',
                )
            }
        )
    )
