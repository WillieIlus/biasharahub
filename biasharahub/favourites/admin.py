from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Bookmark, Vote


class BookmarkResource(resources.ModelResource):
    class Meta:
        model = Bookmark
        fields = ('content_type', 'object_id', 'id', 'user__first_name', 'publish', 'updated',)


class VoteResource(resources.ModelResource):
    class Meta:
        model = Vote
        fields = ('content_type', 'object_id', 'id', 'user__first_name', 'publish', 'updated', 'vote')


class BookmarkAdmin(ImportExportModelAdmin):
    resource_class = BookmarkResource


class VoteAdmin(ImportExportModelAdmin):
    resource_class = VoteResource


admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Vote, VoteAdmin)
