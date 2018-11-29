from king_admin import king_admin_base
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.shortcuts import render,Http404
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from king_admin import forms
from django.contrib.auth import login,authenticate,logout
from django.core.cache import cache
from king_admin import util
from king_admin.permissions.permission import check_permission
from king_admin import views_base
from backconf import redis_cli

REDIS_CONN=redis_cli.redis_conn()

def acc_login(request):
    response=views_base.Login(request,'king_admin','管理员').acc_login()
    return response


@login_required(login_url="/king_admin/login/")
def acc_logout(request):
    logout(request)
    return redirect('/king_admin/login/')



@login_required(login_url="/king_admin/login/")
def app_index(request):
    menus=views_base.MenuList(request).adminmenus()
    return render(request, 'king_admin/king_admin_index.html',{'menus':menus})



@login_required(login_url="/king_admin/login/")
@check_permission
def table_objs_display(request,app_name,table_name):
    return_data=views_base.TableDisplay(request,app_name,table_name,embed=True).show_table()
    if return_data:
        if type(return_data) is dict:
            return render(request, 'king_admin/king_admin_table_objs.html', return_data)
        else:
            return return_data
    else:
        raise Http404("url %s/%s not found" % (app_name, table_name))


@login_required(login_url="/king_admin/login/")
def edit_table(request,app_name,table_name,num):
    return_data=views_base.TableChange(request, app_name, table_name, num,embed=True,edit=True).edittable()
    if type(return_data) is dict:

        return render(request, 'king_admin/king_admin_table_objs_change.html', return_data)
    else:
        return return_data


@login_required(login_url="/king_admin/login/")
def edit_password(request,app_name,table_name,num):
    admin_class = king_admin_base.site.enabled_admin[app_name][table_name]
    obj=admin_class.models.objects.get(id=num)
    model_form_class = forms.create_modelform(request, admin_class)
    return_url_path = request.path.replace('/password/','/')
    errors=''
    if request.method=='POST':
        _pwd1=request.POST.get('password1')
        _pwd2=request.POST.get('password2')
        if _pwd1==_pwd2:
            obj.set_password(_pwd1)
            obj.save()
            return redirect(request.path.replace('/password/','/'))
        else:
            errors='两次输入密码不一致,请重新输入...'
    return render(request, 'king_admin/king_admin_edit_password.html', {'ud':num,
                                                                        'admin_class': admin_class,
                                                                       'obj':obj,
                                                                       'errors':errors,
                                                                       'menus': views_base.MenuList(request).adminmenus(),
                                                                       'app_name': app_name,
                                                                       'table_name': table_name,
                                                                        'return_url_path':return_url_path,
                                                                        })




@login_required(login_url="/king_admin/login/")
def field_delete(request,app_name,table_name,obj_id):
    admin_class = king_admin_base.site.enabled_admin[app_name][table_name]
    if not obj_id.isdigit():
        objs_id_list=request.POST.get('delete_obj').split(',')
        for choice_id in objs_id_list:
            if choice_id.isdigit():
                try:
                    obj=admin_class.models.objects.filter(id=int(choice_id)).first()
                    obj.delete()
                except TypeError as e:
                    errors = '多对多关系表不能删除'
        return redirect('/king_admin/%s/%s' % (app_name, table_name))
    else:
        obj =admin_class.models.objects.get(id=obj_id)
        back_edit_url_path=request.path.replace('/delete/','/change/')
        errors=''
        if request.method=='POST':
            try:
                obj.delete()
                return redirect('/king_admin/%s/%s'%(app_name,table_name))
            except TypeError as e:
                errors='多对多关系表不能删除'
        return render(request, 'king_admin/king_admin_table_objs_delete.html', {"back_edit_url_path":back_edit_url_path,
                                                                   'objs': obj,
                                                                   'admin_class': admin_class,
                                                                   'app_name': app_name,
                                                                   'table_name':table_name,
                                                                   'objs_id':obj_id,
                                                                   'errors':errors,
                                                                   'menus': views_base.MenuList(request).adminmenus(),
                                                                     })




@login_required(login_url="/king_admin/login/")
def table_obj_add(request,app_name,table_name):
    return_data=views_base.DataAdd(request,app_name,table_name,embed=True).add_data()
    if type(return_data) is dict:
        return render(request, 'king_admin/king_admin_table_objs_add.html', return_data)
    else:
        return return_data

