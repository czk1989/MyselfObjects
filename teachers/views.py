from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,authenticate,logout
from king_admin import views_base
from crm import models as crmmodels
# Create your views here.


def teacher_login(request):
    response=views_base.Login(request,'teachers').acc_login()
    return response

def teacher_logout(request):
    logout(request)
    return redirect('/teachers/login/')


def index(request):
    login_teacher=crmmodels.UserProfile.objects.get(email=request.user.email).roles.first()
    teacher=crmmodels.Role.objects.filter(name='teachers').first()
    if login_teacher==teacher:
        # menus=views_base.MenuList(request).shoumenus()
        return render(request, 'teachers/teachers_home.html',)
    else:
        errors='非讲师无法登录该后台系统'
        return render(request,'page_403.html',{'app_name':'teachers','errors':errors})


def my_class(request):
    return render(request, 'teachers/my_classes.html')

def class_stu_list(request,class_id):
    
    print('in PC')
    class_obj = crmmodels.ClassList.objects.get(id=class_id)
    return render(request,'teachers/class_stu_list.html',{'class_ojb':class_obj})

