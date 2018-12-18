
from django.urls import path,re_path
from film import views
app_name='film'
urlpatterns = [
    re_path('^$', views.index,name='film_index'),
    re_path('vip/(?P<area>\w+)/', views.vip,name='vip'),
    path('see/', views.see,name='see'),
    path('register/', views.register,name='register'),
    path('filmlogout/', views.film_logout,name='logout'),
    re_path('^kankan/(?P<num>\d+)/$',views.kankan, name="film_kankan"),
    re_path('^vipkankan/(?P<role>\w+)/(?P<num>\d+)/$',views.vipkankan, name="film_vip_kankan"),

]
