"""robotShopWX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from robotShop_WX import views

urlpatterns = [
    url(r'^wx/wechat/', views.wechat),
    url(r'^wx/open/', views.openDoor),
    url(r'^wx/sendCode/', views.sendCode),
    url(r'^wx/registerByPhone/', views.registerByPhone),
    url(r'^wx/saveUserInfo/', views.saveUserInfo,name='save-user'),
    url(r'^wx/registerSuccess/', views.registerSuccess),
    url(r'^wx/registerFailed/', views.registerFailed),
    url(r'^uploadFile$', views.uploadFile),
    url(r'^MP_verify_JuVs63CDuMTQn8nE\.txt/$', TemplateView.as_view(template_name='MP_verify_JuVs63CDuMTQn8nE.txt',content_type='text/txt')),
]
