from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save

from accounts.models import User

from utility.models import MetaTagsMixin


class Comment( MetaTagsMixin, models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()

    publish = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-publish']

    def replies(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True



def pre_save_comment_receiver(sender, instance, *args, **kwargs):
    # if not instance.slug:
    #     instance.slug = create_slug(instance)
    if not instance.meta_description:
        if instance.content:
            instance.meta_description = instance.content
    if not instance.meta_author:
        if instance.user.first_name:
            instance.meta_author = instance.user.first_name
            instance.meta_copyright = instance.user.first_name
        else:
            instance.meta_author = instance.user
    if not instance.meta_keywords:
        if instance.content_object:
            instance.meta_keywords = instance.content_object






pre_save.connect(pre_save_comment_receiver, sender=Comment)
