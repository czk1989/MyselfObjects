#
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import Http404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.utils import IntegrityError
from crm import models
from king_admin import views_base
from king_admin import king_admin_base
from king_admin import util
from king_admin import forms
#展示销售角色能够查看的数据库表页面


@login_required(login_url="/accounts/crm/login/")
def sales_index(request):
    login_seller=models.UserProfile.objects.get(email=request.user.email).roles.first()
    seller=models.Role.objects.filter(name='sales').first()
    if login_seller==seller:
        menus=views_base.MenuList(request).shoumenus()
        return render(request, 'crm/sales_index.html', {'menus':menus})
    else:
        errors='非销售人员无法登录该后台系统'
        return render(request,'page_403.html',{'app_name':'crm','errors':errors})


@login_required(login_url="/accounts/crm/login/")
def customers(request):
    template_data=views_base.TableDisplay(request,'crm','customer',embed=False).show_table()

    if template_data:
        if type(template_data) is dict:
            return render(request,'crm/customers.html',template_data,)
        else:
            return template_data
    else:
        raise Http404("url %s/%s not found" % ('crm', 'customer'))


@login_required(login_url="/accounts/crm/login/")
def customer_show(request,table_name,customer_num):
    return_data=views_base.TableChange(request, 'crm', table_name, customer_num,embed=False,edit=False).edittable()
    if type(return_data) is dict:
        return render(request, 'crm/customer_show.html', return_data)
    else:
        return return_data


@login_required(login_url="/accounts/crm/login/")
def my_customers(request):
    admin_class = king_admin_base.site.enabled_admin['crm']['customer']
    k, filter_condition = util.table_utils(request, admin_class)
    k, orderby_key = util.table_order(request, k)
    k, search_key = util.table_search(request, k, admin_class)
    object_list=models.UserProfile.objects.filter(email=request.user.email).first().customer_set.all()
    menus = views_base.MenuList(request).shoumenus()
    paginator = Paginator(object_list, 2)  # Show 2 contacts per page
    page = request.GET.get('page')
    query_sets = paginator.get_page(page)

    data = {'admin_class': admin_class,
            'query_sets': query_sets,
            'filter_condition': filter_condition,
            'orderby_key': orderby_key,
            'previous_orderby': request.GET.get('o', ''),
            'search_key': search_key,
            'menus': menus,
            'app_name': 'crm',
            'table_name': 'my_customers',
            }
    return render(request,'crm/my_customer.html',data)


@login_required(login_url="/accounts/crm/login/")
def my_customers_change(request,num):
    return_data=views_base.TableChange(request, 'crm', 'customer', num,embed=False,edit=True).edittable()
    if type(return_data) is dict:
        return render(request, 'crm/my_customers_change.html', return_data)
    else:
        return return_data

@login_required(login_url="/accounts/crm/login/")
def my_customers_add(request):
    return_data=views_base.DataAdd(request,'crm','customer',embed=False).add_data()
    if type(return_data) is dict:
        return render(request, 'crm/my_customers_add.html', return_data)
    else:
        return return_data




@login_required(login_url="/accounts/crm/login/")
def enrollment(request,customerid):

    obj=models.Customer.objects.get(id=customerid)
    enroll_form=forms.EnrooMentForm()
    msg=''
    if request.method=="POST":
        test_id=None
        enroll_form=forms.EnrooMentForm(request.POST)
        msg = "请将此链接发送给客户进行填写：http://localhost:8000/crm/customer/registration/{enroll_id}/"
        if enroll_form.is_valid():
            try:
                enroll_form.cleaned_data['customer']=obj
                a=models.Enrollment.objects.create(**enroll_form.cleaned_data)
                msg=msg.format(enroll_id=a.id)
            except IntegrityError as e:
                enroll_form.add_error('__all__','用户已经存在')
                x=models.Enrollment.objects.get(customerid=obj.id,enrolled_class_id=enroll_form.cleaned_data['enrolled_class'].id)
                msg= msg.format(enroll_id=x.id)
                test_id=x.id
        if models.Enrollment.objects.filter(id=test_id).first():
            if models.Enrollment.objects.filter(id=test_id).first().contract_agreed:
                return redirect('/crm/review/%s/'%test_id)
    return render(request, 'my_crm/enrollment.html', {'enroll_form':enroll_form,
                                                   'customer_name':obj.name,
                                                   'msg':msg,
                                                   'request':request})

