from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from utility.models import Common, MetaTagsMixin


class Category(Common, MetaTagsMixin):
    icon = models.CharField(max_length=256, null=True, blank=True, default="")
    photo = models.ImageField(upload_to='categories/photos', null=True, blank=True)


    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'slug': self.slug})




def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.meta_description:
        if instance.description:
            instance.meta_description = instance.description
    if not instance.meta_keywords:
        if instance.name:
            instance.meta_keywords = instance.name

pre_save.connect(pre_save_category_receiver, sender=Category)
