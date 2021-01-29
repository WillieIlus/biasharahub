from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Country, Location


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        fields = ('id', 'name', 'slug', 'description', 'icon', 'country')


class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource


admin.site.register(Country)
admin.site.register(Location, LocationAdmin)
