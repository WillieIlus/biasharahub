from import_export import resources

from .models import PostPoll


class PostPollResource(resources.ModelResource):
    class Meta:
        model = PostPoll
        fields = (
            'id', 'user', 'name', 'slug', 'publish', 'category')
