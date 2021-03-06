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
from django.urls import path,include,re_path
from MyselfObjects import views




urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', views.myobjects, name='home'),
    path('accounts/logout/', views.sys_logout, ),
    path('accounts/login_choice/', views.login_choice, ),
    re_path('^accounts/(?P<app_name>\w+)/login/$', views.sys_login, ),
    path('king_admin/',include('king_admin.urls')),
    path('crm/',include('crm.urls')),
    path('students/',include('students.urls')),
    path('teachers/',include('teachers.urls')),
    path('film/',include('film.urls')),
    path('tupian/',include('SolaAois.urls')),
    path('news/',include('newsapp.urls')),
]


handler404 = views.page_not_found
handler500 = views.page_error