from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from locations.models import Location


class LocationList(ListView):
    model = Location
    paginate_by = 12
    context_object_name = "location"
    template_name = 'locations/list.html'


class LocationDetail(SingleObjectMixin, ListView):  # this is equivalent to DetailView with Pagination
    model = Location
    context_object_name = "location"
    template_name = 'locations/detail.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Location.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.company.all()


class LocationCreate(LoginRequiredMixin, CreateView):
    model = Location
    fields = '__all__'
    template_name = 'includes/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = " Add Location "
        return context


class LocationUpdate(LoginRequiredMixin, UpdateView):
    model = Location
    fields = '__all__'
    template_name = 'includes/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = " Update Location "
        return context
