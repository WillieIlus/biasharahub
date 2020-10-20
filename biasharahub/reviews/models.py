from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify

from accounts.models import User
from comments.models import Comment
from favourites.models import Vote
from hitcount.models import Hit
from utility.models import UrlMixin

RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class Review(UrlMixin, models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()

    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    hit_count = GenericRelation(Hit)
    comments = GenericRelation(Comment)
    votes = GenericRelation(Vote, related_query_name='review')

    class Meta:
        unique_together = ('object_id', 'user')
        # unique_together = ('company', 'user')
        ordering = ['-publish']

    def save(self, *args, **kwargs):
        slug = slugify("%s at  %s" % (self.user, self.content_object))
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('reviews:detail', kwargs={'slug': self.slug})

    def get_url_path(self):
        return reverse('reviews:detail', kwargs={'slug': self.slug})

    @cached_property
    def image_count(self):
        return self.photos.count()

    @cached_property
    def featured_image(self):
        return self.photos.all().first()


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='photos')
    img = models.ImageField(upload_to='business/review_photos', null=True)
    alt = models.CharField(max_length=256, null=True, default="")

    def __str__(self):
        return self.img.url
