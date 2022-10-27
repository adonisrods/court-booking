"""formbooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from accounts.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',send_otp,name="login"),
    path('',send_otp),
    re_path(r'^verifyotp/(?P<phone>\d+)/',verify_otp,name="verifyotp"),
    re_path(r'^dashbord/(?P<phone>\d+)/',dashbord, name="dashbord"),
    re_path(r'^booking/(?P<phone>\d+)/(?P<ground_name>\D+)/(?P<date>\d+)/',booking,name="booking"),
    re_path(r'^bookingconfirm/(?P<phone>\d+)/(?P<id>\d+)/',bookingconfirm,name="bookingconfirm"),
    re_path(r'^cancelconfirm/(?P<phone>\d+)/(?P<id>\d+)/',cancelconfirm,name="cancelconfirm"),
    re_path(r'^booked/(?P<phone>\d+)/',booked,name="booked"),
    re_path(r'^already_booked/(?P<phone>\d+)/',already_booked,name="already_booked")
]
