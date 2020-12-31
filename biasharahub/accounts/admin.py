from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from accounts.resource import UserResource
from .models import User, Network, SocialProfile


class SocialProfileInline(admin.TabularInline):
    model = SocialProfile
    extra = 6


class AccountAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    inlines = [SocialProfileInline]


admin.site.register(User, AccountAdmin)
admin.site.register(Network)


