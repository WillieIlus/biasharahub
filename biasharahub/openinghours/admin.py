from django.contrib import admin

from .models import OpeningHours, ClosingRules


class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 0


class ClosingRulesInline(admin.StackedInline):
    model = ClosingRules
    extra = 0

