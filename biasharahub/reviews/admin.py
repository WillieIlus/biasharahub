from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from reviews.resource import ReviewResource
from .models import Review, ReviewImage


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 6


class ReviewAdmin(ImportExportModelAdmin):
    resource_class = ReviewResource
    inlines = [ReviewImageInline]


admin.site.register(Review, ReviewAdmin)
