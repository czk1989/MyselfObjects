
from django.urls import path,re_path
from teachers import views
app_name='teachers'
urlpatterns = [
    re_path('^$',views.index,name='tea_index'),
    re_path('^my_class/$', views.my_class, name='my_class'),
    re_path('^my_class/(?P<class_id>\d+)/stu_list/$', views.class_stu_list, name='class_stu_list'),

]
