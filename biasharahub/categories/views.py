from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from business.forms import SocialProfileFormSet
from business.models import Business
from categories.forms import CategoryForm, CategoryBusinessForm
from categories.models import Category


class CategoryList(ListView):
    model = Category
    paginate_by = 12
    context_object_name = "category"
    template_name = 'categories/list.html'


class CategoryDetail(SingleObjectMixin, ListView):
    model = Category
    context_object_name = "category"
    template_name = 'categories/detail.html'
    paginate_by = 15

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.company.all()


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'includes/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = " Add Category "
        return context


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'includes/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = " Update Category "
        return context


class CategoryBusinessCreate(LoginRequiredMixin, CreateView):
    model = Business
    form_class = CategoryBusinessForm
    template_name = 'business/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['social_form'] = SocialProfileFormSet(self.request.POST)

        else:
            context['social_form'] = SocialProfileFormSet()

        return context

    def form_valid(self, form):
        form.instance.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        form.save()

        context = self.get_context_data(form=form)
        social_form = context['social_form']

        if social_form.is_valid():
            response = super().form_valid(form)
            social_form.instance = self.object
            social_form.save()
            return response
        else:
            return super().form_invalid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        print('the is an error in your form')
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('business:detail', kwargs={'slug': self.object.slug})
