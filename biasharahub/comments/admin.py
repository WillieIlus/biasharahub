from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Comment


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
        fields = ('content_type', 'object_id', 'id', 'user__first_name', 'content', 'parent__id', 'publish', 'updated',)


class CommentAdmin(ImportExportModelAdmin):
    resource_class = CommentResource


admin.site.register(Comment, CommentAdmin)
