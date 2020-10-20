from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView

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

    # def get_initial(self):
    #     initial = super().get_initial()
    #     choices = OpeningHours.weekday.choices
    #     initial['weekday'] = OpeningHours.object.filter(choices=choices)
    #     # initial['weekday'] = OpeningHours.weekday.choices
    #     return initial


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

#
# @login_required
# def opening_hours(request, slug):
#     company = Business.objects.get(slug=slug)
#
#     if request.method == "POST":
#         formset = openingHoursFormset(
#             # request.POST, request.FILES,
#             instance=company, initial=[{'weekday': x} for x in range(1, 8)])
#         if formset.is_valid():
#             formset.save()
#             messages.success(request, "Successfully Created")
#             return HttpResponseRedirect(company.get_absolute_url())
#     else:
#         formset = openingHoursFormset(instance=company,
#                                       initial=[{'weekday': x} for x in range(1, 8)]
#                                       )
#
#     context = {
#         "formset": formset,
#     }
#     return render(request, "openinghours/formset.html", context)
