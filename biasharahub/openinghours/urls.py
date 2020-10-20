from django.urls import path

from openinghours.views import OpeningHoursUpdateView

app_name = 'openinghours'

urlpatterns = [
    # path('<slug:slug>/update2/', opening_hours, name='update2'),
    path('<slug:slug>/opening_hours/', OpeningHoursUpdateView.as_view(), name='update'),
    # path('<slug:slug>//', OpeningHoursUpdateView.as_view(), name='opening_hours_update'),
]
