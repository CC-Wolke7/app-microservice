from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .choices import Breed
from .models import Favorite, Offer, OfferImage, Subscription, User


class FavoriteInline(admin.TabularInline):
    model = Favorite

    fields = ["offer"]

    extra = 0


class SubscriptionInline(admin.TabularInline):
    model = Subscription

    fields = ["breed"]

    extra = 0
    max_num = len(Breed.choices)


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
        [
            None, {
                "fields": [
                    "name",
                    "email",
                    "uuid",
                    "password",
                    "description",
                    "profile_image_name",
                ],
            }
        ],
        [
            "Django Permissions", {
                "classes": ["collapse"],
                "fields": [
                    "is_staff", "is_superuser", "groups", "user_permissions"
                ]
            }
        ],
    ]

    inlines = [FavoriteInline, SubscriptionInline]


class OfferImageInline(admin.TabularInline):
    model = OfferImage

    fields = ["name"]

    extra = 0


class OfferAdmin(admin.ModelAdmin):
    fields = [
        "uuid", "date_published", "published_by", "name", "age", "species",
        "breed", "sex", "sterile", "description", "location"
    ]
    readonly_fields = ["uuid", "date_published", "published_by"]
    list_display = ["name", "species", "breed", "published_by", "uuid"]

    inlines = [OfferImageInline]


admin.site.register(User, UserAdmin)
admin.site.register(Offer, OfferAdmin)
