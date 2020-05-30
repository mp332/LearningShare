from django.conf.urls import url
from .import views

from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'AccountApp'

urlpatterns = [
    url('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name="user_login"),
    url("new-login/", auth_views.LoginView.as_view, {"template_name": "account/login.html"}),
    url('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name="user_logout"),
    url("logout/", auth_views.LoginView.as_view, {"template_name": "account/logout.html"}, name="user_logout"),
    url(r'^register/$', views.register, name="user_register"),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'),
         {"post_change_redirect": "account/password-change-done"}, name='password_change'),
    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),
         name='account/password_change_done'),
    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html", success_url=reverse_lazy('account:password_reset_done'),
        email_template_name='account/password_reset_email.html', subject_template_name='account/password_reset_subject.txt'),  name="password_reset"),
    url(r'^password-reset-done/$', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
        name="password_reset_done"),
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html", success_url=reverse_lazy('account:password_reset_complete')),
        name="password_reset_confirm"),
    url(r'^password-reset-complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
        name="password_reset_complete"),

    url(r'^my-information/$', views.myself, name="my_information"),
    url(r'^edit-my-information/$', views.myself_edit, name="edit_my_information"),
    url(r'^my-image/$', views.my_image, name="my_image"),
    url(r'^my-collections/$', views.my_collect, name="my_collections")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)