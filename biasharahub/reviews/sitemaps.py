from django.contrib.sitemaps import Sitemap

from .models import Review


class ReviewSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.8

    def items(self):
        return Review.objects.all()

    def lastmod(self, obj):
        return obj.publish
