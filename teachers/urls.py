
from django.contrib import admin
from django.urls import path,include,re_path
from teachers import views
app_name='teachers'
urlpatterns = [
    re_path('^$',views.index,name='tea_index'),
    re_path('^login/$', views.teacher_login, name='teacher_login'),
    re_path('^logout/$', views.teacher_logout, name='teacher_logout'),
    re_path('^my_class/$', views.my_class, name='my_class'),
    # re_path('^registered/$', views.registered, name='stu_registered'),
    # re_path('^jump/$', views.jump),
    # re_path('^classlist/$', views.classlist,name='classlist'),
    # re_path('^my_course/$', views.my_course,name='my_course'),
    # re_path('^payment/$', views.payment,name='payment'),
    # re_path('^studyrecord/$', views.studyrecord,name='studyrecord'),
    # re_path('^enrollment/(?P<classlist_id>\d+)/$', views.enrollment, name="enrollment"),
    # re_path('^pay/(?P<enroll_id>\d+)/$', views.pay, name="pay"),
]
