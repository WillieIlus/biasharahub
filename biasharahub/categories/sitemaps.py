from django.contrib.sitemaps import Sitemap

from .models import Category


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.publish
