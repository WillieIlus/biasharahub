from django.urls import path

from .views import CommentList, CommentDetail, CommentEdit, CommentReview, CommentReviewBusiness, CommentPostPoll

app_name = 'comments'

urlpatterns = [
    path('', CommentList.as_view(), name='list'),
    path('<slug:slug>/', CommentDetail.as_view(), name='detail'),
    path('<slug:slug>/new/', CommentReview.as_view(), name='new'),
    path('<slug:slug>/poll_comment/', CommentPostPoll.as_view(), name='poll_comment'),
    path('<slug:slug>/new_comment/', CommentReviewBusiness.as_view(), name='new_comment'),
    path('<slug:slug>/edit/', CommentEdit.as_view(), name='edit'),

]
