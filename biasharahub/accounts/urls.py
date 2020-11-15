from django.urls import path

from .views import Dashboard, Detail, UserUpdateView, hide_mail, hide_phone, SocialProfile

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('<pk>/', Detail.as_view(), name='detail'),
    path('<pk>/show_hide/', hide_mail, name='show_hide'),
    path('<pk>/show_hide_phone/', hide_phone, name='show_hide_phone'),
    path('settings/account_edit/', UserUpdateView.as_view(), name='account_edit'),
    # path('<pk>/social_profile/', SocialProfile.as_view(), name='social_profile'),

]
