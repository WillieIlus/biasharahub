# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class HitManager(models.Manager):

    def get_for_object(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        hit_count, created = self.get_or_create(
            content_type=ctype, object_pk=obj.pk)
        return hit_count

    def filter_active(self, *args, **kwargs):
        grace = getattr(settings, 'HITCOUNT_KEEP_HIT_ACTIVE', {'days': 7})
        period = timezone.now() - timedelta(**grace)
        return self.filter(created__gte=period).filter(*args, **kwargs)
