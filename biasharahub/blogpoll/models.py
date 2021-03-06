from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from accounts.models import User
from categories.models import Category
from comments.models import Comment
from favourites.models import Vote
from hitcount.models import HitCount
from hitcount.models import HitCountMixin
from utility.models import Common, UrlMixin, MetaTagsMixin


class SameTags(TaggedItemBase):
    content_object = models.ForeignKey('PostPoll', on_delete=models.PROTECT)


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class PostPoll(Common, UrlMixin, MetaTagsMixin, HitCountMixin):
    """
    post
    """
    user = models.ForeignKey(User, related_name='post_by', on_delete=models.PROTECT)
    image = models.ImageField(upload_to="PostPoll/images", blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="category_poll", blank=True)
    tags = TaggableManager(through=SameTags, blank=True, verbose_name='tags')
    rank = models.PositiveIntegerField(blank=True, null=True, )
    conclusion = models.TextField(blank=True, null=True)
    comments = GenericRelation(Comment)
    hit_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return '%s: %s' % (self.name, self.get_status_display())

    class Meta:
        """
                Blogpost's meta informations.
                """
        verbose_name = "post poll"
        verbose_name_plural = "post polls"
        ordering = ['-rank', '-publish', 'name']
        get_latest_by = '-publish'
        permissions = (('can_view_all', 'Can view all entries'),
                       ('can_change_status', 'Can change status'),
                       ('can_change_author', 'Can change author(s)'), )

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def get_url_path(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)

    @property
    def get_vote_count(self):
        pass

    def get_meta_image(self):
        if self.image:
            return self.image.url

    @property
    def previous_entry(self):
        """
        Returns the previous published post if exists.
        """
        return self.get_previous_by_publish()

    @property
    def next_entry(self):
        """
        Returns the next published post if exists.
        """
        return self.get_next_by_publish()


def pre_save_postpoll_receiver(sender, instance, *args, **kwargs):
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


pre_save.connect(pre_save_postpoll_receiver, sender=PostPoll)


class PostChoice(Common):
    poll = models.ForeignKey(PostPoll, related_name='choices', on_delete=models.CASCADE)
    votes = GenericRelation(Vote, related_name='vote_choice')
    user = models.ForeignKey(User, related_name='choice_by', blank=True, null=True, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="Postchoice/images", blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    rank = models.PositiveIntegerField(blank=True, null=True, )
    comments = GenericRelation(Comment)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    #
    def __str__(self):
        return f"{self.poll.name[:25]} - {self.description[:25]}"
