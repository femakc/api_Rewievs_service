from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'confirm_code',
    ]
    add_fieldsets =(
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'bio',
                    'role',
                    # 'confirm_code',
                )
            }
        )
    )

    fieldsets =(
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'bio',
                    'role',
                    # 'confirm_code',
                )
            }
        )
    )

# admin.site.register(CustomUser)
