from django.contrib.sitemaps import Sitemap
# from django.views.generic import TemplateView
from .models import PostPoll


class PostSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.9

    def items(self):
        return PostPoll.objects.all()

    def lastmod(self, obj):
        return obj.publish


#
#
# class Sitemap(TemplateView):
#     """
#     Sitemap view of the Weblog.
#     """
#     template_name = 'zinnia/sitemap.html'
#
#     def get_context_data(self, **kwargs):
#         """
#         Populate the context of the template
#         with all published entries and all the categories.
#         """
#         context = super(Sitemap, self).get_context_data(**kwargs)
#         context.update(
#             {'entries': Entry.published.all(),
#              'categories': Category.published.all(),
#              'authors': Author.published.all()}
#         )
#         return context
