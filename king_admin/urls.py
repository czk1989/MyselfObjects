
from django.contrib import admin
from django.urls import path,re_path
app_name='king_admin'
from king_admin import views
urlpatterns = [
    path('login/', views.acc_login),
    path('logout/', views.acc_logout, name='acc_logout'),
    path('', views.app_index, name="table_index"),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/$', views.table_objs_display,name='table_objs'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<num>\d+)/change/$', views.edit_table,name='edit_detail'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<num>\d+)/change/password/$', views.edit_password,name='change_pwd'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<obj_id>\w+)/delete/$', views.field_delete,name='obj_field_delete'),
    re_path('^(?P<app_name>\w+)/(?P<table_name>\w+)/add/$', views.table_obj_add,name='table_obj_add'),

]
