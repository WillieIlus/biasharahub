from django.urls import path

from .views import PostPollList, PostPollDetail, PostPollCreate, PostPollEdit, PostChoicesView, vote_up, \
    vote_down

app_name = 'post'

urlpatterns = [
    path('', PostPollList.as_view(), name='list'),
    path('new/', PostPollCreate.as_view(), name='new'),
    path('<slug:slug>/add_choice/', PostChoicesView.as_view(), name='add_choice'),
    path('<slug:slug>/vote_up/', vote_up, name='vote_up'),
    path('<slug:slug>/vote_down/', vote_down, name='vote_down'),
    path('<slug:slug>/edit/', PostPollEdit.as_view(), name='edit'),
    path('<slug:slug>/', PostPollDetail.as_view(), name='detail'),

]
