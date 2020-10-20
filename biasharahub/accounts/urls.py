from django.urls import path

from .views import Dashboard, Detail, UserUpdateView

app_name = 'accounts'

urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'),
    # path('activate/<str:uid>/<str:token>', Activate.as_view(), name='activate'),
    #
    # path('signup1/', SignUpView.as_view(), name='register'),
    # path('login/', UserLogin.as_view(), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('<pk>/', Detail.as_view(), name='detail'),
    # path('<pk>/logout/', UserLogout.as_view(), name='logout'),
    # path('reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
    #                                                     email_template_name='accounts/password_reset_email.html',
    #                                                     subject_template_name='accounts/password_reset_subject.txt'),
    #      name='password_reset'),
    # path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
    #      name='password_reset_confirm'),
    # path('reset/complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
    #      name='password_reset_complete'),
    path('settings/account_edit/', UserUpdateView.as_view(), name='account_edit'),
    # path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',
    #                                                                  success_url=reverse_lazy(
    #                                                                      'accounts:password_change_done')),
    #      name='password_change'),
    # path('settings/password/done/',
    #      auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
    #      name='password_change_done'),
]
