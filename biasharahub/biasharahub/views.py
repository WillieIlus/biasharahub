from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.db.models import Count, Avg
from django.shortcuts import redirect
from django.views.generic import TemplateView

from business.models import Business
from categories.models import Category
from comments.forms import CommentForm
from locations.models import Location
from reviews.forms import ReviewForm
from reviews.models import Review


class Home(TemplateView):
    model = Business
    context_object_name = 'home'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = self.model.objects.exclude(photos__isnull=True).annotate(
            avg_reviews=Avg('reviews__rating'),
            num_reviews=Count('reviews')).order_by('-publish',
                                                   '-num_reviews',
                                                   '-avg_reviews',
                                                   'hit_count')[:9]
        context['location'] = Location.objects.annotate(num_companies=Count('company')).order_by('-num_companies')
        context['category'] = Category.objects.annotate(num_companies=Count('company')).order_by('-num_companies')[:6]
        context['category_one'] = Category.objects.annotate(num_companies=Count('company')).order_by('-num_companies')[
                                  :4]
        context['review'] = Review.objects.filter(review_approved=True).order_by('-publish')[:12]
        context['review_form'] = ReviewForm()
        context['comment_form'] = CommentForm()

        return context


class SubscribeForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('subscribe_btn', 'Subscribe'))


class UnSubscribeForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('unsubscribe_btn', 'unSubscribe'))


class NewsletterView(TemplateView):
    subcribe_form_class = SubscribeForm
    unsubcribe_form_class = UnSubscribeForm
    template_name = "includes/newsletter.html"

    def get(self, request, *args, **kwargs):
        kwargs.setdefault("subscribe_form", self.subcribe_form_class())
        kwargs.setdefault("unsubscribe_form", self.unsubcribe_form_class())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_args = {
            'data': self.request.POST,
            'files': self.request.FILES,
        }

        if "subscribe_btn" in request.POST:
            form = self.subcribe_form_class(**form_args)
            if not form.is_valid():
                return self.get(request, subscribe_form=form)
            return redirect("success_form1")
        elif "unsubscribe_btn" in request.POST:
            form = self.unsubcribe_form_class(**form_args)
            if not form.is_valid():
                return self.get(request, unsubscribe_form=form)
            return redirect("success_form2")
        return super().get(request)
