
from django.urls import path,re_path
from students import views
app_name='students'
urlpatterns = [
    re_path('^$',views.stu_index,name='stu_index'),
    re_path('^registered/$', views.registered, name='stu_registered'),
    re_path('^jump/$', views.jump,name='jump'),
    re_path('^classlist/$', views.classlist,name='classlist'),
    re_path('^my_course/$', views.my_course,name='my_course'),
    re_path('^payment/$', views.payment,name='payment'),
    re_path('^studyrecord/$', views.studyrecord,name='studyrecord'),
    re_path('^enrollment/(?P<classlist_id>\d+)/$', views.enrollment, name="enrollment"),
    re_path('^pay/(?P<enroll_id>\d+)/$', views.pay, name="pay"),
]
