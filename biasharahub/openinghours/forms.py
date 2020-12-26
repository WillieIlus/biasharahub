from datetime import time

from django import forms
from django.forms import ModelForm

from openinghours.models import OpeningHours


def str_to_time(s):
    """ Turns strings like '08:30' to time objects """
    return time(*[int(x) for x in s.split(':')])


def time_to_str(t):
    """ Turns time objects to strings like '08:30' """
    return t.strftime('%H:%M')


def time_choices():
    """Return digital time choices every half hour from 00:00 to 23:30."""
    hours = list(range(0, 24))
    times = []
    for h in hours:
        hour = str(h).zfill(2)
        times.append(hour + ':00')
        times.append(hour + ':30')
    return list(zip(times, times))


TIME_CHOICES = time_choices()


class Slot(forms.Form):
    opens = forms.ChoiceField(choices=TIME_CHOICES)
    shuts = forms.ChoiceField(choices=TIME_CHOICES)


class OpeningHoursForm(ModelForm):
    # weekday = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}))
    start = forms.ChoiceField(choices=TIME_CHOICES, label='Opening', required=False)
    end = forms.ChoiceField(choices=TIME_CHOICES, label='Closing', required=False)

    def __init__(self, *args, disabled_weekday=True, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['weekday'].disabled = disabled_weekday

    class Meta:
        model = OpeningHours
        # fields = ('start', 'end', 'closed')
        fields = ('company', 'weekday', 'start', 'end')

