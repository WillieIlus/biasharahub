from allauth.account.models import EmailAddress
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from accounts.resource import UserResource, EmailResource
from .models import User, Network, SocialProfile


class SocialProfileInline(admin.TabularInline):
    model = SocialProfile
    extra = 6


class AccountAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    inlines = [SocialProfileInline]


class EmeailAdmin(ImportExportModelAdmin):
    resource_class = EmailResource


admin.site.register(User, AccountAdmin)
# admin.site.register(EmailAddress, EmeailAdmin)
admin.site.register(Network)
