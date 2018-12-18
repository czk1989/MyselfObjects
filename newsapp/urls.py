
from django.urls import path,re_path
from newsapp import views
app_name='newsapp'
urlpatterns = [
    re_path('^$', views.index,name='news_index'),
    # re_path('^customer/$',views.customers, name="customers"),
    # re_path('^my_customers/$',views.my_customers, name="my_customers"),
    # re_path('^my_customers/add/$', views.my_customers_add, name='customer_add'),
    # re_path('^my_customers/(?P<num>\d+)/change/$',views.my_customers_change, name="my_customers_change"),
    # re_path('^(?P<table_name>\w+)/(?P<customer_num>\d+)/show/$', views.customer_show,name='customer_show'),

]
