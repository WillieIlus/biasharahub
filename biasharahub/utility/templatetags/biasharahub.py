from django.db.models import Count, Avg
from django.template import Library
from requests import Request

from accounts.forms import CustomLoginForm, CustomSignupForm
from accounts.models import User
from business.forms import BusinessAddForm
from business.models import Business
from categories.models import Category
from comments.models import Comment
from openinghours.views_edit import OpeningHoursEditView
from reviews.models import Review

register = Library()


@register.inclusion_tag('tags/categories.html')
def get_categories(count=5):
    return {'categories': Category.objects.annotate(num_companies=Count('company')).order_by('-num_companies')[:count]}
    # return {'categories': Category.objects.order_by('company.count')[:count]}


@register.inclusion_tag('tags/login.html')
def get_login():
    return {'login': CustomLoginForm()}


@register.inclusion_tag('includes/cat_to_add_biz.html')
def get_cat_to_add_biz():
    return {'categories': Category.objects.all}


@register.inclusion_tag('includes/business_form.html', takes_context=True)
def get_business_form():
    form = BusinessAddForm()
    return {
        'form': form,
    }


@register.inclusion_tag('openinghours/edit_form.html')
def get_edit_opening_form():
    return {'opening': OpeningHoursEditView()}


@register.inclusion_tag('tags/signup.html')
def get_signup():
    return {'signup': CustomSignupForm()}


@register.inclusion_tag('tags/users.html')
def get_users():
    return {'authors': User.objects.all()}


@register.inclusion_tag('tags/business_recent.html')
def get_recent_business(number=5):
    return {'business': Business.objects.all()[:number]}


@register.inclusion_tag('tags/reviews_recent.html')
def get_recent_reviews(number=5):
    return {'reviews': Review.objects.all()[:number]}


@register.inclusion_tag('tags/comments_recent.html')
def get_recent_comments(number=5):
    return {'comments': Comment.objects.all()[:number]}


@register.inclusion_tag('tags/business_popular.html')
def get_popular_business(number=5):
    return {'popular_business': Business.objects.annotate(avg_reviews=Avg('reviews__rating'),
                                                          num_reviews=Count('reviews')).order_by(
        '-num_reviews', '-avg_reviews', 'hit_count', '-publish')[:number]}


@register.inclusion_tag('tags/reviews_popular.html')
def get_popular_reviews(number=5):
    return {'popular_reviews': Review.objects.order_by('-comments')[:number]}


# @register.inclusion_tag('tags/related_business.html')
# def get_related_business(number=5):
#     return {'related_business': Business.objects.all()[:number]}
# return {'related_business': Business.services.similar_objects[:number]}


@register.inclusion_tag('tags/statistics.html')
def Biashara_statistics():
    business_count = Business.objects.count()
    reviews_count = Review.objects.count()
    user_count = User.objects.count()
    categories_count = Category.objects.count()
    comments_count = Comment.objects.count()

    return {
        'business_count': business_count,
        'reviews_count': reviews_count,
        'user_count': user_count,
        'categories_count': categories_count,
        'comments_count': comments_count,
    }
