from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'confirmation_code',
    ]
    add_fieldsets = (
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
                    # 'confirmation_code',
                )
            }
        )
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'bio',
                    'role',
                    'confirmation_code',
                )
            }
        )
    )
