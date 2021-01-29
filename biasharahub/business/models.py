from __future__ import unicode_literals

from statistics import mean

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from accounts.models import User, Network
from categories.models import Category
from favourites.models import Bookmark
from hitcount.models import HitCount
from hitcount.models import HitCountMixin
from locations.models import Location
from reviews.models import Review
from utility.models import Common, UrlMixin, MetaTagsMixin


class SameServices(TaggedItemBase):
    content_object = models.ForeignKey('Business', on_delete=models.PROTECT)


class Business(Common, UrlMixin, MetaTagsMixin, HitCountMixin):
    user = models.ForeignKey(User, related_name='added_by', on_delete=models.PROTECT)
    logo = models.ImageField(upload_to="business/logos", blank=True, null=True)
    email = models.EmailField(help_text="This is required", blank=True, null=True)
    website = models.URLField(blank=True, null=True, help_text="Please start with 'https://www.'")
    category = models.ManyToManyField(Category, related_name="company", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, related_name='company', blank=True, null=True,
                                 help_text="Please leave empty if 100% virtual",
                                 on_delete=models.PROTECT)
    services = TaggableManager(through=SameServices, blank=True, verbose_name='services')
    verified = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    hide_mail = models.BooleanField(default=True)
    hide_phone = models.BooleanField(default=True)

    reviews = GenericRelation(Review, related_query_name='reviews')
    bookmark = GenericRelation(Bookmark, related_query_name='bookmarks')
    hit_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        verbose_name = "biashara"
        verbose_name_plural = "biasharas"

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.reviews.all()))

        if not all_ratings:
            return float('nan');
        else:
            return mean(all_ratings)

    def get_absolute_url(self):
        return reverse('business:detail', kwargs={'slug': self.slug})

    def get_url_path(self):
        return reverse('business:detail', kwargs={'slug': self.slug})

    def can_edit(self, request):
        if request.user is self.user:
            can_edit = True
            return can_edit
        else:
            can_edit = False
            return can_edit

    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)

    @cached_property
    def image_count(self):
        return self.photos.count()

    @cached_property
    def featured_image(self):
        return self.photos.all().first()


def pre_save_business_receiver(sender, instance, *args, **kwargs):
    # if not instance.slug:
    #     instance.slug = create_slug(instance)
    if not instance.meta_description:
        if instance.description:
            instance.meta_description = instance.description
    if not instance.meta_author:
        if instance.user.first_name:
            instance.meta_author = instance.user.first_name
            instance.meta_copyright = instance.user.first_name
        else:
            instance.meta_author = instance.user
    if not instance.meta_keywords:
        if instance.name:
            instance.meta_keywords = instance.name


pre_save.connect(pre_save_business_receiver, sender=Business)


class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='photos')
    img = models.ImageField(upload_to='business/photos', null=True, blank=True)
    alt = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.img.url

    _metadata = {
        'image': 'get_meta_image',
    }

    def get_meta_image(self):
        if self.img:
            return self.img.url


class CompanySocialProfile(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='network')
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    username = models.CharField(max_length=254)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.username
