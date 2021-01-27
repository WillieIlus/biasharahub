from import_export import resources

from business.models import Business


class BusinessResource(resources.ModelResource):
    class Meta:
        model = Business
        fields = (
        'id', 'user', 'name', 'slug', 'logo', 'email', 'phone', 'description', 'website', 'location__name',
        'category__name', 'address', 'services')
