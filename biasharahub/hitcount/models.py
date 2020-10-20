# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

from .managers import HitManager
from .signals import delete_hit_count


@receiver(delete_hit_count)
def delete_hit_count_handler(sender, instance, save_hit=False, **kwargs):
    if not save_hit:
        instance.hit.decrease()


class Hit(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    ip = models.CharField(max_length=40, editable=False, db_index=True)
    session = models.CharField(max_length=40, editable=False, db_index=True)
    user_agent = models.CharField(max_length=255, editable=False)
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, editable=False, on_delete=models.CASCADE)

    hits = models.PositiveIntegerField(default=0)

    content_type = models.ForeignKey(ContentType, related_name="content_type_set_for_%(class)s",
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = HitManager()

    class Meta:
        ordering = ('-hits', '-created',)
        get_latest_by = ('created', 'modified')
        verbose_name = _("hit")
        verbose_name_plural = _("hits")
        unique_together = ("content_type", "object_id")

    def __str__(self):
        return '%s' % self.content_object

    def increase(self):
        self.hits = F('hits') + 1
        self.save()

    def decrease(self):
        self.hits = F('hits') - 1
        self.save()

    def hits_in_last(self, **kwargs):
        assert kwargs, "Must provide at least one timedelta arg (eg, days=1)"

        period = timezone.now() - timedelta(**kwargs)
        return self.hit_set.filter(created__gte=period).count()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.hit.increase()

        super(Hit, self).save(*args, **kwargs)

    def delete(self, save_hit=False):
        delete_hit_count.send(
            sender=self, instance=self, save_hit=save_hit)
        super(Hit, self).delete()


class BlacklistIP(models.Model):
    ip = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = "hit_blacklist_ip"
        verbose_name = _("Blacklisted IP")
        verbose_name_plural = _("Blacklisted IPs")

    def __str__(self):
        return '%s' % self.ip


class BlacklistUserAgent(models.Model):
    user_agent = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "hit_blacklist_user_agent"
        verbose_name = _("Blacklisted User Agent")
        verbose_name_plural = _("Blacklisted User Agents")

    def __str__(self):
        return '%s' % self.user_agent
