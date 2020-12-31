from import_export import resources

from business.models import Business


class BusinessResource(resources.ModelResource):
    class Meta:
        model = Business
