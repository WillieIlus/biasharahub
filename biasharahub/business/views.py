from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet

from business.models import Business, BusinessImage
from comments.forms import CommentForm
from reviews.forms import ReviewForm
from .forms import BusinessForm, BusinessSearchForm, \
    SocialProfileFormSet, BusinessPhotoForm, BusinessNameForm


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(
        content_auto=request.GET.get(
            'query',
            ''))[
          :5]
    s = []
    for result in sqs:
        d = {"value": result.name, "data": result.object.slug}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)


class FacetedSearchView(BaseFacetedSearchView):
    form_class = BusinessSearchForm
    facet_fields = ['category', 'location']
    template_name = 'business/search_result.html'
    paginate_by = 10
    context_object_name = 'object_list'


class BusinessList(ListView):
    paginate_by = 10
    context_object_name = "business"
    template_name = 'business/list.html'

    def get_queryset(self):
        return Business.objects.order_by('-publish')


class BusinessCreate(LoginRequiredMixin, CreateView):
    model = Business
    form_class = BusinessForm
    template_name = 'business/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['social_form'] = SocialProfileFormSet(self.request.POST)

        else:
            context['social_form'] = SocialProfileFormSet()

        return context

    def form_valid(self, form):
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


class BusinessEdit(LoginRequiredMixin, UpdateView):
    model = Business
    form_class = BusinessForm
    template_name = 'business/form.html'

    def get_context_data(self, **kwargs):
        context = super(BusinessEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['social_form'] = SocialProfileFormSet(self.request.POST, instance=self.object)
            context['social_form'].full_clean()
        else:
            context['social_form'] = SocialProfileFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['social_form']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class BusinessSocialProfile(LoginRequiredMixin, UpdateView):
    model = Business
    form_class = BusinessNameForm
    template_name = 'business/form.html'
    # success_url = self.model.get_absolute_url
    success_message = "updated successfully"

    def get_success_url(self):
        return reverse('business:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['social_form'] = SocialProfileFormSet(self.request.POST, instance=self.object)
            context['social_form'].full_clean()

        else:
            context['social_form'] = SocialProfileFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        # form.instance.user = self.request.user
        # form.save()

        context = self.get_context_data(form=form)
        formset = context['social_form']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


BusinessPhotoFormSet = inlineformset_factory(Business, BusinessImage, form=BusinessPhotoForm, extra=6, max_num=12,
                                             can_delete=True)


#
# class ManagePhoto(LoginRequiredMixin, UpdateView):
#     model = Business
#     form_class = BusinessNameForm
#     template_name = 'business/formset.html'
#     success_message = "created successfully"
#
#     # def get_object(self):  # and you have to override a get_object method
#     #     return get_object_or_404(Business, slug=self.request.GET.get('slug'))
#
#     def get_success_url(self):
#         return reverse('business:detail', kwargs={'slug': self.object.slug})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['photo_formset'] = BusinessPhotoFormSet(instance=self.object, data=self.request.POST, files=self.request.FILES)
#             context['photo_formset'].full_clean()
#         else:
#             context['photo_formset'] = BusinessPhotoFormSet(instance=self.object)
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data(form=form)
#         formset = context['photo_formset']
#         if formset.is_valid():
#             response = super().form_valid(self.request.FILES)
#             formset.instance = self.object
#             formset.save()
#             return response
#         else:
#             return super().form_invalid(form)
#

@login_required
def add_photos(request, slug):
    """company = get_object_or_404(Business, slug=slug)"""
    company = Business.objects.get(slug=slug)
    form = BusinessPhotoFormSet(request.POST or None, request.FILES or None, instance=company)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(company.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "business/photo_formset.html", context)


class BusinessDetail(SingleObjectMixin, ListView):
    model = Business
    template_name = 'business/detail.html'
    context_object_name = 'business'
    slug_field = 'slug'
    paginate_by = 10
    count_hit = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Business.objects.all())
        return super().get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Business, slug=uri_to_iri(slug))

    def get_queryset(self):
        return self.object.reviews.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        context['comment_form'] = CommentForm()

        return context


class PhotoGallery(DetailView):
    model = Business
    template_name = 'business/photo_gallery.html'
    context_object_name = 'photo'
