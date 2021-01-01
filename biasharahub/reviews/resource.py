from import_export import resources

from reviews.models import Review


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = (
            'content_type', 'object_id', 'id', 'user__first_name', 'publish', 'updated', 'slug', 'rating')
