from django.urls import path
from favourites.views import bookmark_company

from .views import BusinessCreate, BusinessDetail, BusinessList, BusinessEdit, PhotoGallery, \
    FacetedSearchView, autocomplete, BusinessSocialProfile, add_photos, hide_mail, hide_phone, AddCategory

app_name = 'business'

urlpatterns = [
    path('new/', BusinessCreate.as_view(), name='new'),
    path('list/', BusinessList.as_view(), name='list'),

    path('', FacetedSearchView.as_view(), name='search'),

    path('<slug:slug>/', BusinessDetail.as_view(), name='detail'),
    path('<slug:slug>/edit/', BusinessEdit.as_view(), name='edit'),
    path('<slug:slug>/add_category/', AddCategory.as_view(), name='add_category'),
    path('<slug:slug>/social_profile/', BusinessSocialProfile.as_view(), name='social_profile'),
    path('<slug:slug>/photo_update/', add_photos, name='photo_update'),
    path('<slug:slug>/gallery/', PhotoGallery.as_view(), name='gallery'),
    path('<slug:slug>/show_hide/', hide_mail, name='show_hide'),
    path('<slug:slug>/show_hide_phone/', hide_phone, name='show_hide_phone'),

    path('<slug:slug>/bookmark/', bookmark_company, name='bookmark'),
    path('autocomplete/', autocomplete),

]
