from django.contrib import admin

from openinghours.admin import ClosingRulesInline
from openinghours.models import OpeningHours
from .models import BusinessImage, Business, CompanySocialProfile


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0


class BusinessImageInline(admin.TabularInline):
    model = BusinessImage
    extra = 6


class CompanyAdmin(admin.ModelAdmin):
    inlines = [OpeningHoursInline, ClosingRulesInline]
    search_fields = ['name', 'slug']


admin.site.register(Business, CompanyAdmin)
admin.site.register(BusinessImage)
admin.site.register(CompanySocialProfile)
