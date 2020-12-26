from django.urls import path
from openinghours.views_edit import OpeningHoursEditView

from openinghours.views import CurrentlyOpenView
from openinghours.views import OpeningHoursUpdateView

app_name = 'openinghours'

urlpatterns = [
    path('<slug:slug>/opening_hours/', OpeningHoursUpdateView.as_view(), name='update'),
    path('', CurrentlyOpenView.as_view(), name='openinghours_currently_open'),
    path('edit/<slug:slug>/', OpeningHoursEditView.as_view(), name='openinghours_edit'),
    # path('edit/<int:pk>', OpeningHoursEditView.as_view(), name='openinghours_edit'),
]
