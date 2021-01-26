from django.urls import path

from .views import LocationCreate, LocationDetail, LocationList, LocationUpdate

app_name = 'locations'

urlpatterns = [
    path('new/', LocationCreate.as_view(), name='new'),
    path('<slug:slug>/', LocationDetail.as_view(), name='detail'),
    # path('<slug:location_slug>/<slug:category_slug>/', CategoryLocationDetail.as_view(), name='detail'),
    path('<slug:slug>/edit/', LocationUpdate.as_view(), name='edit'),

    path('', LocationList.as_view(), name='list'),

]
