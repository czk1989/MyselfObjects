from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from backconf.permissions.permission import check_permission
from crm import models as crmmodels

@login_required(login_url="/accounts/teachers/login/")
@check_permission
def index(request):
    if request.user.roles.first().name=='manager':
        return redirect('/king_admin/')
    return render(request, 'teachers/teachers_index.html', )


@login_required(login_url="/accounts/teachers/login/")
@check_permission
def my_class(request):

    return render(request, 'teachers/my_classes.html')


@login_required(login_url="/accounts/teachers/login/")
@check_permission
def class_stu_list(request,class_id):
    class_obj = crmmodels.ClassList.objects.get(id=class_id)
    return render(request,'teachers/class_stu_list.html',{'class_ojb':class_obj})

