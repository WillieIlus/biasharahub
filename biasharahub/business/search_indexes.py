from django.utils import timezone
from haystack import indexes

from .models import Business


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True,
                                  template_name='business/business_text.txt'
                                  )
    name = indexes.EdgeNgramField(model_attr='name')
    description = indexes.EdgeNgramField(model_attr="description", null=True)
    category = indexes.CharField(model_attr='category', faceted=True)
    location = indexes.CharField(model_attr='location', faceted=True)

    # for auto complete
    content_auto = indexes.EdgeNgramField(model_attr='name')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Business

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(publish__lte=timezone.now())
