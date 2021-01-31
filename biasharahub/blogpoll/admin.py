# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import PostChoice, PostPoll
from .resource import PostPollResource


class PostChoiceInline(admin.TabularInline):
    model = PostChoice
    extra = 6


class PostPollAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'publish']
    list_display_links = ['name']
    # list_editable = ['publish']
    list_filter = ['publish', 'updated']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name', 'publish']

    resource_class = PostPollResource
    inlines = [PostChoiceInline]


admin.site.register(PostPoll, PostPollAdmin)
