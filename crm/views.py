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

def crm_login(request):
    response=views_base.Login(request,'crm').acc_login()
    return response

@login_required(login_url="/crm/login/")
def crm_logout(request):
    logout(request)
    return redirect('/crm/login/')


@login_required(login_url="/crm/login/")
def sales_home(request):
    login_seller=models.UserProfile.objects.get(email=request.user.email).roles.first()
    seller=models.Role.objects.filter(name='sales').first()
    if login_seller==seller:
        menus=views_base.MenuList(request).shoumenus()
        return render(request, 'crm/sales_home.html',{'menus':menus})
    else:
        errors='非销售人员无法登录该后台系统'
        return render(request,'page_403.html',{'app_name':'crm','errors':errors})


@login_required(login_url="/crm/login/")
def customers(request):
    template_data=views_base.TableDisplay(request,'crm','customer',embed=False).show_table()

    if template_data:
        if type(template_data) is dict:
            return render(request,'crm/customers.html',template_data,)
        else:
            return template_data
    else:
        raise Http404("url %s/%s not found" % ('crm', 'customer'))

def customer_show(request,table_name,customer_num):
    return_data=views_base.TableChange(request, 'crm', table_name, customer_num,embed=False,edit=False).edittable()
    if type(return_data) is dict:
        return render(request, 'crm/customer_show.html', return_data)
    else:
        return return_data

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

def my_customers_change(request,num):
    return_data=views_base.TableChange(request, 'crm', 'customer', num,embed=False,edit=True).edittable()
    if type(return_data) is dict:
        return render(request, 'crm/my_customers_change.html', return_data)
    else:
        return return_data


def my_customers_add(request):
    return_data=views_base.DataAdd(request,'crm','customer',embed=False).add_data()
    if type(return_data) is dict:
        return render(request, 'crm/my_customers_add.html', return_data)
    else:
        return return_data





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



# def enrollment(request,num):
#     obj=models.Customer.objects.get(id=num)
#     enroll_form=forms.EnrooMentForm()
#     msg=''
#     if request.method=="POST":
#         test_id=None
#         enroll_form=forms.EnrooMentForm(request.POST)
#         msg = "请将此链接发送给客户进行填写：http://localhost:8000/crm/customer/registration/{enroll_id}/"
#         if enroll_form.is_valid():
#             try:
#                 enroll_form.cleaned_data['customer']=obj
#                 a=models.Enrollment.objects.create(**enroll_form.cleaned_data)
#                 msg=msg.format(enroll_id=a.id)
#             except IntegrityError as e:
#                 enroll_form.add_error('__all__','用户已经存在')
#                 x=models.Enrollment.objects.get(customer_id=obj.id,enrolled_class_id=enroll_form.cleaned_data['enrolled_class'].id)
#                 msg= msg.format(enroll_id=x.id)
#                 test_id=x.id
#         if models.Enrollment.objects.filter(id=test_id).first():
#             if models.Enrollment.objects.filter(id=test_id).first().contract_agreed:
#                 return redirect('/crm/review/%s/'%test_id)
#     return render(request, 'my_crm/enrollment.html', {'enroll_form':enroll_form,
#                                                    'customer_name':obj.name,
#                                                    'msg':msg,
#                                                    'request':request})
#
# def stu_registration(request,num):
#     enroll_obj=models.Enrollment.objects.get(id=num)
#
#     if request.method=='POST':
#         if request.is_ajax():
#             print(request.FILES)
#             enroll_data_dir='%s/%s'%(settings.ENROLLED_DATA,enroll_obj.id)
#             if not os.path.exists(enroll_data_dir):
#                 os.makedirs(enroll_data_dir,exist_ok=True)
#             for k,file_obj in request.FILES.items():
#                 with open('%s/%s'%(enroll_data_dir,file_obj),'wb') as f:
#                     for chunk in file_obj.chunks():
#                         f.write(chunk)
#         customer_form=forms.CustomerForm(request.POST,instance=enroll_obj.customer)
#         if customer_form.is_valid():
#             customer_form.save()
#             enroll_obj.contract_agreed=True
#             enroll_obj.save()
#             status=1
#             return render(request, 'my_crm/registration.html', {'status':status})
#     else:
#         customer_form = forms.CustomerForm(instance=enroll_obj.customer)
#
#     return render(request, 'my_crm/registration.html', {'customer_form':customer_form,
#                                                      'enroll_obj':enroll_obj})
#
#
# def reviews(request,num):
#     enroll_obj = models.Enrollment.objects.get(id=num)
#     enroll_form=forms.EnrooMentForm(instance=enroll_obj)
#     customer_obj = forms.CustomerForm(instance=enroll_obj.customer)
#     return render(request, 'my_crm/reviews.html', {'customer_obj':customer_obj,
#                                                 'enroll_form':enroll_form,
#                                                 'enroll_obj':enroll_obj})
#
#
#
# def return_enroll(request,num):
#     enroll_obj=models.Enrollment.objects.get(id=num)
#     enroll_obj.contract_agreed=False
#     enroll_obj.save()
#     return redirect('/crm/customer/registration/%s/'%num)
#
# def payment(request,num):
#     payment_form=forms.PaymentForm()
#     enroll_obj=models.Enrollment.objects.get(id=num)
#     msg=''
#     if request.method=="POST":
#         if 'amount' in request.POST:
#             if request.POST['amount'].isdigit():
#                 amount=int(request.POST['amount'])
#                 if amount<500:
#                     msg='金额太少'
#                 else:
#                     payment_obj=models.Payment.objects.\
#                         create(customer=enroll_obj.customer,course=enroll_obj.enrolled_class.course,amount=amount)
#                     payment_obj.save()
#                     enroll_obj.contract_approved=True
#                     enroll_obj.save()
#                     customer_obj=enroll_obj.customer
#                     customer_obj.status=1
#                     customer_obj.save()
#
#                     return redirect('/king_admin/')
#             else:
#                 msg='请输入正确的金额格式'
#         else:
#             msg='SB，想黑我'
#
#     return render(request, 'my_crm/pay.html', {'enroll_obj':enroll_obj,
#                                                 'msg':msg, })
#

