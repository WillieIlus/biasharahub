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
    from_hour = models.TimeField(_('Start'), default='8:00', null=True, blank=True )
    to_hour = models.TimeField(_('End'), default='18:00', null=True, blank=True)
    # closed = models.BooleanField(verbose_name=_('Closed'))

    class Meta:
        verbose_name = _('Opening Hours')
        verbose_name_plural = _('Opening Hours')
        ordering = ['company', 'weekday', 'from_hour']

    def __str__(self):
        return _("%(premises)s %(weekday)s (%(start)s - %(to_hour)s)") % {
            'premises': self.company,
            'weekday': self.weekday,
            'start': self.from_hour,
            'to_hour': self.to_hour
        }


class ClosingRules(models.Model):
    """
    Used to overrule the OpeningHours. This will "close" the store due to
    public holiday, annual closing or private party, etc.
    """
    class Meta:
        verbose_name = _('Closing Rule')
        verbose_name_plural = _('Closing Rules')
        ordering = ['start']

    company = models.ForeignKey(Business, verbose_name=_('company'), related_name='closing_rules',
                                on_delete=models.CASCADE)
    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))
    reason = models.TextField(_('Reason'), null=True, blank=True)

    def __str__(self):
        return _("%(premises)s is closed from %(start)s to %(end)s\
        due to %(reason)s") % {
            'premises': self.company.name,
            'start': str(self.start),
            'end': str(self.end),
            'reason': self.reason
        }

