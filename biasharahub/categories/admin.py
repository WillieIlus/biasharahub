from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'icon')


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource


admin.site.register(Category, CategoryAdmin)
