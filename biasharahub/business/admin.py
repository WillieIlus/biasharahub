from django.contrib import admin

from openinghours.models import OpeningHours
from .models import BusinessImage, Business, CompanySocialProfile


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    inlines = [OpeningHoursInline]
    search_fields = ['name', 'slug']


admin.site.register(Business, CompanyAdmin)
admin.site.register(BusinessImage)
admin.site.register(CompanySocialProfile)
