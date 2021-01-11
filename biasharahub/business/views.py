from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import uri_to_iri
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet

from accounts.decorators import UserRequiredMixin
from biasharahub import settings
from business.models import Business, BusinessImage
from comments.forms import CommentForm
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from reviews.forms import ReviewForm
from .forms import BusinessForm, BusinessSearchForm, \
    SocialProfileFormSet, BusinessPhotoForm, BusinessNameForm, AddCategoryForm, BusinessAddForm


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
    # context_object_name = 'business'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context


class BusinessList(ListView):
    paginate_by = 10
    context_object_name = "business"
    template_name = 'business/list.html'

    def get_queryset(self):
        return Business.objects.annotate(avg_reviews=Avg('reviews__rating'), num_reviews=Count('reviews')).order_by(
            '-num_reviews', '-avg_reviews', 'hit_count', '-publish')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()

        return context


class BusinessCreate(LoginRequiredMixin, CreateView):
    model = Business
    form_class = BusinessAddForm
    template_name = 'business/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # form.save()
        messages.success(self.request,
                         'Awesome! you have successfully created your biashara, '
                         'you can now see how great it is. You can update it to give your clients more info.')

        return super().form_valid(form)


class BusinessEdit(LoginRequiredMixin, UserRequiredMixin, UpdateView):
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


class AddCategory(LoginRequiredMixin, UserRequiredMixin, UpdateView):
    model = Business
    form_class = AddCategoryForm
    template_name = 'business/form.html'


class BusinessSocialProfile(LoginRequiredMixin, UserRequiredMixin, UpdateView):
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


class BusinessDetail(SingleObjectMixin, HitCountMixin, ListView):
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
        context['related_business'] = self.object.services.similar_objects()
        # context['biashara'] = self.model.objects.first()
        context['timezone'] = settings.TIME_ZONE

        if self.object:
            hit_count = get_hitcount_model().objects.get_for_object(self.object)
            hits = hit_count.hits
            context['hitcount'] = {'pk': hit_count.pk}

            if self.count_hit:
                hit_count_response = self.hit_count(self.request, hit_count)
                if hit_count_response.hit_counted:
                    hits = hits + 1
                context['hitcount']['hit_counted'] = hit_count_response.hit_counted
                context['hitcount']['hit_message'] = hit_count_response.hit_message

            context['hitcount']['total_hits'] = hits

        return context


class PhotoGallery(DetailView):
    model = Business
    template_name = 'business/photo_gallery.html'
    context_object_name = 'photo'


def hide_mail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    hidden = business.hide_mail

    if hidden:
        business.hide_mail = False
        business.save()
    else:
        business.hide_mail = True
        business.save()

    return HttpResponseRedirect(business.get_absolute_url())


def hide_phone(request, slug):
    business = get_object_or_404(Business, slug=slug)
    hidden = business.hide_phone
    if hidden:
        business.hide_phone = False
        business.save()
    else:
        business.hide_phone = True
        business.save()

    return HttpResponseRedirect(business.get_absolute_url())
