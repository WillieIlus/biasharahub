from import_export import resources

from reviews.models import Review


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
