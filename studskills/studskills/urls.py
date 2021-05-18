"""studskills URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,  PasswordResetConfirmView, \
    PasswordResetCompleteView


from module.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('analyzer/', submit_process, name='analyzer'),
    path('deepcode_login/', dc_login, name='dc_login'),
    path('analyzer/result/', submit_process, name='result'),
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', LogoutUserView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/password_reset', PasswordResetView.as_view(
        template_name='registration/reset_password.html',
        subject_template_name='registration/reset_subject.txt',
        email_template_name='registration/reset_email.txt',
    ), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
             template_name='registration/email_sent.html'
         ), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/confirm_password.html',
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_confirmed.html'
    ), name='password_reset_complete'),
]
