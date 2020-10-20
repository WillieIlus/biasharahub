import datetime

from django.template import Library
from django.utils import timezone

from accounts.forms import CustomLoginForm, CustomSignupForm
from accounts.models import User
from business.models import Business
from categories.models import Category
from comments.models import Comment
from reviews.models import Review

register = Library()


@register.inclusion_tag('tags/categories.html')
def get_categories(count=5):
    return {'categories': Category.objects.order_by('-publish')[:count]}


@register.inclusion_tag('tags/login.html')
def get_login():
    return {'login': CustomLoginForm()}


@register.inclusion_tag('includes/cat_to_add_biz.html')
def get_cat_to_add_biz():
    return {'categories': Category.objects.order_by('-publish')}


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
    return {'popular_business': Business.objects.order_by('-reviews')[:number]}


@register.inclusion_tag('tags/reviews_popular.html')
def get_popular_reviews(number=5):
    return {'popular_reviews': Review.objects.order_by('-comments')[:number]}


@register.inclusion_tag('tags/related_business.html')
def get_related_business(number=5):
    return {'related_business': Business.objects.all()[:number]}
    # return {'related_business': Business.objects.services.similar_objects[:number]}


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


@register.simple_tag()
def is_open():
    """
    Is the company currently open? Pass "now" to test with a specific
    timestamp. Can be used stand-alone or as a helper.
    """
    now = timezone.now()
    open = Business.objects.first().opening_hours.all()  # .filter(closed=False, start__lte=now, end__gte=now,
    # weekday=now.isoweekday)
    for oh in open:
        is_open = False
        if oh.weekday == now.isoweekday() and oh.start <= now <= oh.end:
            is_open = oh

        if is_open is not False:
            return oh
    return False


@register.simple_tag()
def is_open_now(self):
    now = timezone.now()
    if self.is_closed_for_now:
        return False

    now_time = datetime.time(now.hour, now.minute, now.second)
    # now_time = datetime.time()
    #
    ohs = self.opening_hours.all()
    for oh in ohs:
        is_open = False
        # start and end is on the same day
        if oh.weekday == now.isoweekday() and oh.start <= now_time <= oh.end:
            is_open = oh

        # start and end are not on the same day and we test on the start day
        if oh.weekday == now.isoweekday() and oh.start <= now_time and (
                (oh.end < oh.start) and (now_time < datetime.time(23, 59, 59))):
            is_open = oh

        # start and end are not on the same day and we test on the end day
        if oh.weekday == (now.isoweekday() - 1) % 7 and oh.start >= now_time and now_time <= oh.end < oh.start:
            is_open = oh
            # print " 'Special' case after midnight", oh

        if is_open is not False:
            return oh
    return False
