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


def acc_login(request):
    response=views_base.Login(request,'king_admin').acc_login()
    return response
    # errors={}
    # if request.method=="POST":
    #     _name=request.POST.get('email')
    #     _password=request.POST.get('password')
    #
    #     #_verify_code和_verify_code_key暂时还未设置，为None
    #     _verify_code = request.POST.get('verify_code')
    #     _verify_code_key=request.POST.get('verify_code_key')
    #     # print(_verify_code,_verify_code_key)
    #     if cache.get(_verify_code_key) == _verify_code:
    #         user = authenticate(username=_name, password=_password)
    #         if user:
    #             login(request,user)
    #             # request.session.set_expiry(60 * 600)
    #             return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/king_admin/")
    #         else:
    #             errors['error']='Wrong user or password'
    #     else:
    #         errors['error'] = '验证码错误'
    # return render(request, 'king_admin/login.html', {'errors':errors})



@login_required(login_url="/king_admin/login/")
def acc_logout(request):
    logout(request)
    return redirect('/king_admin/login/')



@login_required(login_url="/king_admin/login/")
def app_index(request):
    menus=views_base.MenuList(request).adminmenus()
    #
    # for k,v in menus.items():
    #     print(k,v)
        # print(k.name)
    return render(request, 'king_admin/king_admin_index.html',{'menus':menus})

# def app_tables(request,app_name):
#     enabled_admins = {app_name:king_admin_base.site.enabled_admin[app_name]}
#     # return render(request, 'crm/app_index.html',{'enabled_admins':enabled_admins,'current_app':app_name})
#     return HttpResponse('ok')



@login_required(login_url="/king_admin/login/")
@check_permission
def table_objs_display(request,app_name,table_name):

    # if app_name in king_admin_base.site.enabled_admin:
    #     if table_name in king_admin_base.site.enabled_admin[app_name]:
    #         admin_class=king_admin_base.site.enabled_admin[app_name][table_name]
    #         object_list,filter_condition=util.table_utils(request, admin_class)
    #         object_list,orderby_key=util.table_order(request, object_list)
    #         object_list,search_key=util.table_search(request, object_list, admin_class)
    #         if request.method=='POST':
    #             selected_ids=request.POST.get('selected_list')
    #             action=request.POST.get('action')
    #             if selected_ids:
    #                 selected_objs=admin_class.models.objects.filter(id__in=selected_ids.split(','))
    #             else:
    #                 raise KeyError('No object selected')
    #             if hasattr(admin_class,action):
    #                 action_func=getattr(admin_class,action)
    #                 return action_func(admin_class,request,selected_objs,king_admin_base.site.enabled_admin)
    #
    #         paginator = Paginator(object_list,2)  # Show 25 contacts per page
    #         page = request.GET.get('page')
    #         query_sets = paginator.get_page(page)
    #
    #         return_data={'admin_class':admin_class,
    #                      'query_sets':query_sets,
    #                      'filter_condition':filter_condition,
    #                      'orderby_key':orderby_key,
    #                      'previous_orderby':request.GET.get('o',''),
    #                      'search_key':search_key,
    #                      'table_list': king_admin_base.site.enabled_admin,
    #                      'app_name':app_name,
    #                      'table_name': table_name,
    #                      }
    #         if not embed:
    #             return render(request, 'king_admin/king_admin_table_objs.html',return_data)
    #         else:
    #             return return_data

    # else:
    #     raise Http404("url %s/%s not found" % (app_name, table_name))

    # print('ok')
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
    # admin_class = king_admin_base.site.enabled_admin[app_name][table_name]
    # admin_class.read_only = True
    # model_form_class=forms.create_modelform(request,admin_class)
    # change_table_data=admin_class.models.objects.get(id=num)
    #
    # delete_url_path = request.path.replace('/change/', '/delete/')
    # return_url_path='/king_admin/%s/%s/'%(app_name,table_name)
    #
    # form_obj = model_form_class(instance=change_table_data)
    # if request.method=='POST':
    #     form_obj=model_form_class(request.POST,instance=change_table_data)
    #     if form_obj.is_valid():
    #         form_obj.save()
    #         return redirect(request.path.replace('/%s/change/'%num, '/'))
    return_data=views_base.TableChange(request, app_name, table_name, num,embed=True,edit=True).edittable()
    if type(return_data) is dict:

        return render(request, 'king_admin/king_admin_table_objs_change.html', return_data)
    else:
        return return_data
    # return render(request, 'king_admin/king_admin_table_objs_change.html', {'form_obj':form_obj,
    #                                                              'admin_class': admin_class,
    #                                                              'delete_url_path': delete_url_path,
    #                                                              'return_url_path':return_url_path,
    #                                                              'menus': views_base.MenuList(request).adminmenus(),
    #                                                              'app_name': app_name,
    #                                                             'table_name':table_name
    #                                                              })




@login_required(login_url="/king_admin/login/")
def edit_password(request,app_name,table_name,num):
    admin_class = king_admin_base.site.enabled_admin[app_name][table_name]
    obj=admin_class.models.objects.get(id=num)
    model_form_class = forms.create_modelform(request, admin_class)
    # model_form_class = admin_class.add_form()
    # print(model_form_class)
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
    # admin_class = king_admin_base.site.enabled_admin[app_name][table_name]
    # admin_class.read_only = False
    # model_form_class = forms.create_modelform(request, admin_class)
    # if request.method=='POST':
    #     form_obj=model_form_class(request.POST)
    #     if form_obj.is_valid():
    #         form_obj.save()
    #         return redirect(request.path.replace('/add/','/'))
    # else:
    #     form_obj=model_form_class()
    # return render(request, 'king_admin/king_admin_table_objs_add.html', {'form_obj':form_obj,
    #                                                         'admin_class':admin_class,
    #                                                         'menus': views_base.MenuList(request).adminmenus(),
    #                                                         'app_name': app_name,
    #                                                         'table_name': table_name
    #                                                           })
    return_data=views_base.DataAdd(request,app_name,table_name,embed=True).add_data()
    if type(return_data) is dict:
        return render(request, 'king_admin/king_admin_table_objs_add.html', return_data)
    else:
        return return_data