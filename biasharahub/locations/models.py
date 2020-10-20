from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utility.models import Common


class Country(Common):
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "countries"

    def get_absolute_url(self):
        return reverse("country:detail", kwargs={"slug": self.slug})


class Location(Common):
    icon = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey(Country, related_name='country', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "locations"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("locations:detail", kwargs={"slug": self.slug})
