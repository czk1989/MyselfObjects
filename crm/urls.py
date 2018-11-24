
from django.urls import path,re_path
from crm import views
app_name='crm'
urlpatterns = [
    re_path('^$', views.sales_home,name='crm'),
    re_path('^login/$', views.crm_login,name='crm_login'),
    re_path('^logout/$', views.crm_logout,name='crm_logout'),
    re_path('^customer/$',views.customers, name="customers"),
    re_path('^my_customers/$',views.my_customers, name="my_customers"),
    re_path('^my_customers/add/$', views.my_customers_add, name='customer_add'),
    re_path('^my_customers/(?P<num>\d+)/change/$',views.my_customers_change, name="my_customers_change"),
    re_path('^(?P<table_name>\w+)/(?P<customer_num>\d+)/show/$', views.customer_show,name='customer_show'),
    re_path('^enrollment/(?P<customerid>\d+)/$', views.enrollment, name="enrollment"),

]
