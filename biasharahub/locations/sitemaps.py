from django.contrib.sitemaps import Sitemap

from .models import Location


class LocationSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Location.objects.all()

    def lastmod(self, obj):
        return obj.publish
