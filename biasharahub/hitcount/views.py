# -*- coding: utf-8 -*-

import warnings
from collections import namedtuple

from django.conf import settings

from hitcount.models import Hit, BlacklistIP, BlacklistUserAgent
from hitcount.utils import RemovedInHitCount13Warning
from hitcount.utils import get_ip


class HitCountMixin(object):
    """
    Mixin to evaluate a HttpRequest and a HitCount and determine whether or not
    the HitCount should be incremented and the Hit recorded.
    """

    @classmethod
    def hit_count(self, request, hitcount):
        """
        Called with a HttpRequest and HitCount object it will return a
        namedtuple:

        UpdateHitCountResponse(hit_counted=Boolean, hit_message='Message').

        `hit_counted` will be True if the hit was counted and False if it was
        not.  `'hit_message` will indicate by what means the Hit was either
        counted or ignored.
        """
        UpdateHitCountResponse = namedtuple(
            'UpdateHitCountResponse', 'hit_counted hit_message')

        # as of Django 1.8.4 empty sessions are not being saved
        # https://code.djangoproject.com/ticket/25489
        if request.session.session_key is None:
            request.session.save()

        user = request.user
        try:
            is_authenticated_user = user.is_authenticated()
        except:
            is_authenticated_user = user.is_authenticated
        session_key = request.session.session_key
        ip = get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        hits_per_ip_limit = getattr(settings, 'HITCOUNT_HITS_PER_IP_LIMIT', 0)
        exclude_user_group = getattr(settings, 'HITCOUNT_EXCLUDE_USER_GROUP', None)

        # first, check our request against the IP blacklist
        if BlacklistIP.objects.filter(ip__exact=ip):
            return UpdateHitCountResponse(
                False, 'Not counted: user IP has been blacklisted')

        # second, check our request against the user agent blacklist
        if BlacklistUserAgent.objects.filter(user_agent__exact=user_agent):
            return UpdateHitCountResponse(
                False, 'Not counted: user agent has been blacklisted')

        # third, see if we are excluding a specific user group or not
        if exclude_user_group and is_authenticated_user:
            if user.groups.filter(name__in=exclude_user_group):
                return UpdateHitCountResponse(
                    False, 'Not counted: user excluded by group')

        # eliminated first three possible exclusions, now on to checking our database of
        # active hits to see if we should count another one

        # start with a fresh active query set (HITCOUNT_KEEP_HIT_ACTIVE)
        qs = Hit.objects.filter_active()

        # check limit on hits from a unique ip address (HITCOUNT_HITS_PER_IP_LIMIT)
        if hits_per_ip_limit:
            if qs.filter(ip__exact=ip).count() >= hits_per_ip_limit:
                return UpdateHitCountResponse(
                    False, 'Not counted: hits per IP address limit reached')

        # create a generic Hit object with request data
        hit = Hit(session=session_key, hitcount=hitcount, ip=get_ip(request),
                  user_agent=request.META.get('HTTP_USER_AGENT', '')[:255], )

        # first, use a user's authentication to see if they made an earlier hit
        if is_authenticated_user:
            if not qs.filter(user=user, hitcount=hitcount):
                hit.user = user  # associate this hit with a user
                hit.save()

                response = UpdateHitCountResponse(
                    True, 'Hit counted: user authentication')
            else:
                response = UpdateHitCountResponse(
                    False, 'Not counted: authenticated user has active hit')

        # if not authenticated, see if we have a repeat session
        else:
            if not qs.filter(session=session_key, hitcount=hitcount):
                hit.save()
                response = UpdateHitCountResponse(
                    True, 'Hit counted: session key')
            else:
                response = UpdateHitCountResponse(
                    False, 'Not counted: session key has active hit')

        return response


def _update_hit_count(request, hitcount):
    """
    Deprecated in 1.2. Use hitcount.views.Hit CountMixin.hit_count() instead.
    """
    warnings.warn(
        "hitcount.views._update_hit_count is deprecated. "
        "Use hitcount.views.HitCountMixin.hit_count() instead.",
        RemovedInHitCount13Warning
    )
    return HitCountMixin.hit_count(request, hitcount)
