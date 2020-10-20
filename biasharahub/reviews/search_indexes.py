# import datetime
#
# from haystack import indexes
#
# from .models import Review
#
#
# class ReviewIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     content = indexes.CharField(model_attr='content')
#     publish = indexes.DateTimeField(model_attr='publish')
#     user = indexes.CharField(model_attr='user')
#     title = indexes.CharField(model_attr='title')
#     rating = indexes.IntegerField(model_attr='rating')
#
#     def get_model(self):
#         return Review
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.filter(publish__lte=datetime.datetime.now())
