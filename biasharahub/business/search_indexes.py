from django.utils import timezone
from haystack import indexes
from .models import Business


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False,
                             template_name='business/business_text.txt'
                             )
    name = indexes.EdgeNgramField(model_attr='name')
    description = indexes.EdgeNgramField(model_attr="description", null=True)
    category = indexes.CharField(model_attr='category', faceted=True)
    location = indexes.CharField(model_attr='location', faceted=True)
    address = indexes.CharField(model_attr='address', faceted=True)
    services = indexes.CharField(model_attr='services', faceted=True)
    date_published = indexes.DateTimeField(model_attr='publish')
    verified= indexes.BooleanField(model_attr='verified', faceted=True)
    # featured= indexes.BooleanField(model_attr='featured', faceted=True)
    #
    # # reviews = indexes.CharField(model_attr='reviews', faceted=True)
    # # bookmark = indexes.FacetCharField(model_attr='bookmark', faceted=True)
    # # hit_count = indexes.FacetCharField(model_attr='hit_count', faceted=True)

    # for auto complete
    content_auto = indexes.EdgeNgramField(model_attr='name')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Business

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(publish__lte=timezone.now())
