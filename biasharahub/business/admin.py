from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from business.resource import BusinessResource
from openinghours.admin import ClosingRulesInline
from openinghours.models import OpeningHours
from .models import BusinessImage, Business, CompanySocialProfile


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0


class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 6


class CompanySocialProfileInline(admin.TabularInline):
    model = CompanySocialProfile
    extra = 6


class BusinessAdmin(ImportExportModelAdmin):
    resource_class = BusinessResource
    inlines = [BusinessImageInline, CompanySocialProfileInline, OpeningHoursInline, ClosingRulesInline]
    search_fields = ['name', 'slug']


admin.site.register(Business, BusinessAdmin)
