from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from king_admin import views_base
from students import models
from students import forms
from students import util
from crm import models as crmmodels



def stu_login(request):
    
    response=views_base.Login(request,'students').acc_login()
    return response

# @login_required(login_url="/student/login/")
def stu_logout(request):
    logout(request)
    return redirect('/students/login/')


def registered(request):
    return_data=views_base.CreatAccount(request,False,'students').redigtered()
    if type(return_data) is dict:
        return render(request,'students/stu_registered.html',return_data)
    else:
        models.Account.objects.create(account=return_data[0],profile=return_data[1])
        return redirect('/students/jump/')


def jump(request):
    return render(request,'students/jump.html')


def stu_index(request):
    login_stu=crmmodels.UserProfile.objects.get(email=request.user.email).roles.first()
    stu=crmmodels.Role.objects.filter(name='students').first()
    if login_stu==stu:
        menus=views_base.MenuList(request).shoumenus()
        return render(request, 'students/students_home.html',{'menus':menus})
    else:
        errors='非销售人员无法登录该后台系统'
        return render(request,'page_403.html',{'app_name':'crm','errors':errors})


def classlist(request):
    menus = views_base.MenuList(request).shoumenus()
    course_list=crmmodels.ClassList.objects.all()
    stu_cum=models.Account.objects.get(account=crmmodels.UserProfile.objects.get(email=request.user.email)).profile
    stu_enroll=stu_cum.enrollment_set.all()
    stu_enroll_dict = {}
    if len(stu_enroll)>0:
        for i in stu_enroll:
            stu_enroll_dict[i.enrolled_class]=i
    course_display = ['id', 'branch', 'course', 'class_type', 'start_date']
    data={
        'course_list':course_list,
        'menus':menus,
        'course_display':course_display,
        'stu_enroll_dict':stu_enroll_dict
        }
    return render(request,'students/course_list.html',data)



def my_course(request):
    menus = views_base.MenuList(request).shoumenus()
    stu=models.Account.objects.filter(account=crmmodels.UserProfile.objects.get(email=request.user.email)).first()
    stu_enrolls=stu.profile.enrollment_set.all()
    stu_classlist=[]
    if len(stu_enrolls)>0:
        for stu_enroll in stu_enrolls:
            if stu_enroll.contract_approved:
                stu_classlist.append(stu_enroll.enrolled_class)
    return render(request,'students/my_course.html',{'menus':menus,
                                                     'stu_classlist':stu_classlist,
                                                     })


def enrollment(request,classlist_id):
    menus = views_base.MenuList(request).shoumenus()
    customer=models.Account.objects.get(account=crmmodels.UserProfile.objects.get(email=request.user.email)).profile
    enrollclass=crmmodels.ClassList.objects.filter(id=classlist_id).first()
    branch=enrollclass.branch.name
    course=enrollclass.course.name
    template=crmmodels.ContractTemplate.objects.filter().first().template
    enroll_form=forms.EnrooMentForm()
    msg=''
    if request.method=="POST":
        enroll_form=forms.EnrooMentForm(request.POST)
        if enroll_form.is_valid():
            enroll_form.cleaned_data['customer']=customer
            enroll_form.cleaned_data['enrolled_class']=enrollclass
            crmmodels.Enrollment.objects.create(**enroll_form.cleaned_data)
        if crmmodels.Enrollment.objects.filter(customer=customer).first():
            enroll_id=crmmodels.Enrollment.objects.filter(customer=customer).first().id
            return redirect('/students/payment/%s/'%enroll_id)
    return render(request, 'students/enrollment.html', {'enroll_form':enroll_form,
                                                   'customer_name':customer.name,
                                                   'customer_email':customer.email,
                                                   'enrollclass':enrollclass,
                                                   'msg':msg,
                                                   'request':request,
                                                    'menus':menus,
                                                        'branch':branch,
                                                        'course':course,
                                                        'template':template
                                                        })


def pay(request,enroll_id):
    menus = views_base.MenuList(request).shoumenus()
    enroll_obj=crmmodels.Enrollment.objects.get(id=enroll_id)
    price=enroll_obj.enrolled_class.price
    payment_form=forms.PaymentForm()
    msg=''
    if request.method=="POST":
        payment_form = forms.PaymentForm(request.POST)
        if 'amount' in request.POST:
            if request.POST['amount'].isdigit():
                amount=int(request.POST['amount'])
                if amount!=int(price):
                    msg='输入金额不对，请重新输入'
                else:
                    if payment_form.is_valid():
                        payment_form.cleaned_data['customer'] = enroll_obj.customer
                        payment_form.cleaned_data['enrollment'] = enroll_obj
                        payment_form.cleaned_data['course'] = enroll_obj.enrolled_class.course
                        crmmodels.Payment.objects.create(**payment_form.cleaned_data)
                        enroll_obj.contract_approved=True
                        enroll_obj.save()
                        customer_obj=enroll_obj.customer
                        customer_obj.status=1
                        customer_obj.save()
                        return redirect('/students/my_course/')
            else:
                msg='请输入正确的格式'
        else:
            msg='SB，想黑我,去你妹的...'
    return render(request, 'students/pay.html', {'enroll_obj':enroll_obj,
                                                     'msg':msg,
                                                     'menus':menus,
                                                     'payment_form':payment_form,
                                                     'price':price,
                                                     })

def payment(request):
    menus = views_base.MenuList(request).shoumenus()
    customer=models.Account.objects.get(account=crmmodels.UserProfile.objects.get(email=request.user.email)).profile
    payment_list=crmmodels.Payment.objects.filter(customer=customer).all()
    condition=False
    if len(payment_list)>0:
        condition=True

    return render(request,'students/payment.html',{'condition':condition,
                                                   'payment_list':payment_list,
                                                   'menus':menus
                                                   })

def studyrecord(request):
    return HttpResponse('正在开发...')
