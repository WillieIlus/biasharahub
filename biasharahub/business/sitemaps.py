from django.contrib.sitemaps import Sitemap

from .models import Business


class BusinessSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Business.objects.all()

    def lastmod(self, obj):
        return obj.publish
