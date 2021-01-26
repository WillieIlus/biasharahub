from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utility.models import Common, MetaTagsMixin


class Country(Common, MetaTagsMixin):
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "countries"

    def get_absolute_url(self):
        return reverse("country:detail", kwargs={"slug": self.slug})


class Location(Common):
    icon = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='location/photos', null=True, blank=True)
    country = models.ForeignKey(Country, related_name='country', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "locations"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse("locations:detail", kwargs={"slug": self.slug})


def pre_save_location_receiver(sender, instance, *args, **kwargs):
    if not instance.meta_description:
        if instance.description:
            instance.meta_description = instance.description
    if not instance.meta_keywords:
        if instance.name:
            instance.meta_keywords = instance.name
