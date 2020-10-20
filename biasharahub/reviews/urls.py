from django.urls import path

from favourites.views import vote_up, vote_down, ReviewVoteUp
from .views import ReviewList, ReviewDetail, ReviewCreate, ReviewEdit, photos

app_name = 'reviews'

urlpatterns = [
    path('', ReviewList.as_view(), name='list'),
    path('<slug:slug>/', ReviewDetail.as_view(), name='detail'),
    path('<slug:slug>/new/', ReviewCreate.as_view(), name='new'),
    path('<slug:slug>/edit/', ReviewEdit.as_view(), name='edit'),
    path('<slug:slug>/photos/', photos, name='photos'),
    path('<slug:slug>/review_like/', ReviewVoteUp.as_view(), name='review_like'),
    path('<slug:slug>/vote_up/', vote_up, name='vote_up'),
    path('<slug:slug>/vote_down/', vote_down, name='vote_down'),

]
