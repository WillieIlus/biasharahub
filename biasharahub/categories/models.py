from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from utility.models import Common


class Category(Common):
    icon = models.CharField(max_length=256, null=True, blank=True, default="")
    photo = models.ImageField(upload_to='category/photos', null=True, blank=True)


    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'slug': self.slug})
