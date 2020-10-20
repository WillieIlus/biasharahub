from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# isoweekday
from business.models import Business

WEEKDAYS = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


class OpeningHours(models.Model):
    company = models.ForeignKey(Business, verbose_name=_('company'), related_name='opening_hours',
                                on_delete=models.CASCADE)
    weekday = models.IntegerField(_('Weekday'), choices=WEEKDAYS)
    start = models.TimeField(_('Start'), default='8:00', null=True, blank=True )
    end = models.TimeField(_('End'), default='18:00', null=True, blank=True)
    closed = models.BooleanField(verbose_name=_('Closed'))

    class Meta:
        verbose_name = _('Opening Hours')
        verbose_name_plural = _('Opening Hours')
        ordering = ['company', 'weekday', 'start']

    def __str__(self):
        return _("%(premises)s %(weekday)s (%(start)s - %(to_hour)s)") % {
            'premises': self.company,
            'weekday': self.weekday,
            'start': self.start,
            'to_hour': self.end
        }
