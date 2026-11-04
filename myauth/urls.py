from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import (
    MyLogoutView,
    set_cookie_view,
    get_cookie_view,
    del_cookie_view,
    set_session_view,
    get_session_view,
    del_session_view,
    AboutMeView,
    RegisterView,
    FooBarView,
    UsersView,
    UserDetailsView,
)

app_name = 'myauth'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('password-change/', PasswordChangeView.as_view(
        template_name='myauth/password-change.html',
        success_url=reverse_lazy("myauth:password_change_done")
    ), name='password_change'),

    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='myauth/password-change-done.html'
    ), name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='myauth/password-reset.html',
        email_template_name="myauth/password_reset_email.html",
        success_url=reverse_lazy("myauth:password_reset_done")
    ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='myauth/password-reset-done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='myauth/password-reset-confirm.html',
        success_url=reverse_lazy("myauth:login")
    ), name='password_reset_confirm'),



    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('users/', UsersView.as_view(), name='users'),
    path('users/<int:pk>/', UserDetailsView.as_view(), name='user'),
    path('cookie/set/', set_cookie_view, name="set_cookie"),
    path('cookie/get/', get_cookie_view, name="get_cookie"),
    path('cookie/del/', del_cookie_view, name="del_cookie"),
    path('session/set/', set_session_view, name="set_session"),
    path('session/get/', get_session_view, name="get_session"),
    path('session/del/', del_session_view, name="del_session"),

    path('foo-bar/', FooBarView.as_view(), name='foo_bar'),
]
