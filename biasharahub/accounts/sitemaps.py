from django.contrib.sitemaps import Sitemap

from .models import User


class AccountsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return User.objects.all()

    def lastmod(self, obj):
        return obj.last_login
