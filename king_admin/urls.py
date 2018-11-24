"""MyselfObjects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
app_name='king_admin'
from king_admin import views
urlpatterns = [
    path('login/', views.acc_login),
    path('logout/', views.acc_logout, name='acc_logout'),
    path('', views.app_index, name="table_index"),
    # re_path('^(?P<app_name>\w+)/$', views.app_tables, name="app_tables"),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/$', views.table_objs_display,name='table_objs'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<num>\d+)/change/$', views.edit_table,name='edit_detail'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<num>\d+)/change/password/$', views.edit_password,name='change_pwd'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<obj_id>\w+)/delete/$', views.field_delete,name='obj_field_delete'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/add/$', views.table_obj_add,name='table_obj_add'),

]
