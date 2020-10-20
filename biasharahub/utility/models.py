from __future__ import unicode_literals

from urllib.parse import urlparse

# import urlparse
from django.conf import settings
from django.db import models
from django.template.defaultfilters import escape
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Common(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True
        ordering = ['publish', 'name']

    _metadata = {
        'title': 'name',
        'description': 'description',
    }

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = slug
        super().save(*args, **kwargs)


class UrlMixin(models.Model):
    """
    A replacement for get_absolute_url()
    Models extending this mixin should have
    either get_url or get_url_path implemented.
    """

    class Meta:
        abstract = True

    def get_url(self):
        if hasattr(self.get_url_path, "dont_recurse"):
            raise NotImplementedError
        try:
            path = self.get_url_path()
        except NotImplementedError:
            raise
        website_url = getattr(
            settings, "DEFAULT_WEBSITE_URL",
            "http://127.0.0.1:8000"
        )
        return website_url + path

    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError
        try:
            url = self.get_url()
        except NotImplementedError:
            raise
        bits = urlparse.urlparse(url)
        return urlparse.urlunparse(("", "") + bits[2:])

    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url_path()


class MetaTagsMixin(models.Model):
    """
    Abstract base class for meta tags in the <head> section
    """
    meta_keywords = models.CharField(_("Keywords"), max_length=255, blank=True,
                                     help_text=_("Separate keywords by comma."), )
    meta_description = models.CharField(_("Description"), max_length=255, blank=True, )
    meta_author = models.CharField(_("Author"), max_length=255, blank=True, )
    meta_copyright = models.CharField(_("Copyright"), max_length=255, blank=True, )

    class Meta:
        abstract = True

    def get_meta_keywords(self):
        tag = ""
        if self.meta_keywords:
            tag = '<meta name="keywords" content="%s" />\n'
            escape(self.meta_keywords)
        return mark_safe(tag)

    def get_meta_description(self):
        tag = ""
        if self.meta_description:
            tag = '<meta name="description" content="%s" />\n' % \
                  escape(self.meta_description)
        return mark_safe(tag)

    def get_meta_author(self):
        tag = ""
        if self.meta_author:
            tag = '<meta name="author" content="%s" />\n' % \
                  escape(self.meta_author)
        return mark_safe(tag)

    def get_meta_copyright(self):
        tag = ""
        if self.meta_copyright:
            tag = '<meta name="copyright" content="%s" />\n' % \
                  escape(self.meta_copyright)
        return mark_safe(tag)

    def get_meta_tags(self):
        return mark_safe("".join((
            self.get_meta_keywords(),
            self.get_meta_description(),
            self.get_meta_author(),
            self.get_meta_copyright(),
        )))
