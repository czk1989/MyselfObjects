
from django.urls import path,re_path
from SolaAois import views
app_name='SolaAois'
urlpatterns = [
    re_path('^$', views.index,name='SolaAois_index'),
    path('meinv/',views.meinv, name="meinv"),
    path('mingxing/',views.mingxing, name="mingxing"),
    re_path('^detail/(?P<role>\w+)/(?P<num>\d+)/$',views.detail, name="detail"),


]
