from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, TemplateView

from biasharahub import settings
from business.forms import BusinessNameForm
from business.models import Business
from openinghours.forms import OpeningHoursForm
from openinghours.models import OpeningHours

openingHoursFormset = inlineformset_factory(Business, OpeningHours, OpeningHoursForm, extra=6, max_num=7,
                                            can_delete=True, can_order=False)


class OpeningHoursUpdateView(LoginRequiredMixin, UpdateView):
    model = Business
    form_class = BusinessNameForm
    is_update_view = True
    template_name = 'openinghours/formset.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = openingHoursFormset(self.request.POST,
                                                     instance=self.object,
                                                     # initial=[{'weekday': x} for x in self.get_initial()['weekday']]
                                                     )
            context['formset'].full_clean()
        else:
            context['formset'] = openingHoursFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class CurrentlyOpenView(TemplateView):
    model = Business
    template_name = "openinghours/index.html"

    def get_context_data(self, **kwargs):
        context = super(CurrentlyOpenView, self).get_context_data(**kwargs)
        context['biashara'] = self.model.objects.all()
        context['timezone'] = settings.TIME_ZONE
        return context
