from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    readonly_fields = ["uuid"]
    ordering = ["name"]

    add_fieldsets = [
        [
            None, {
                "classes": ["wide"],
                "fields": ["name", "password1", "password2"],
            }
        ],
    ]

    list_display = ["email", "name", "uuid"]
    search_fields = ["email", "name", "uuid"]
    list_filter = ["is_staff"]

    fieldsets = [
        [None, {
            "fields": ["name", "email", "uuid", "password"],
        }],
        [
            "Django Permissions", {
                "classes": ["collapse"],
                "fields": [
                    "is_staff", "is_superuser", "groups", "user_permissions"
                ]
            }
        ],
    ]


admin.site.register(User, UserAdmin)
