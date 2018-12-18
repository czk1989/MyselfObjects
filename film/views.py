
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
import uuid
from . import utils
import json,os

DIR=os.path.abspath(__file__)
file_menu=os.path.join(os.path.dirname(DIR),'menu.txt')
file=open(file_menu,'r',encoding='utf-8')
menu=json.load(file)
file.close()
vipname=['111','22','333','444','555']


def index(request):
    if request.session.get('user_id', False):
        return redirect('/film/vip/xxx/')
    else:
        return redirect('/film/see/')


def see(request):

    examp = [i for i in range(100)]
    ret_data = utils.DianYing(request, examp, role=None).kankan_page()

    if request.method == "POST":
        var_email=request.POST.get('InputEmail')
        var_pwd=request.POST.get('InputName')
        user = authenticate(username=var_email, password=var_pwd)
        if user:
            if str(var_email).strip() in vipname:
                request.session['user_id']=str(uuid.uuid4())
                request.session.set_expiry(7200)
                login(request, user)
                return redirect('/film/vip/xxx/')
            else:
                return render(request, 'film/film_index.html', ret_data)
        else:
            return render(request, 'film/film_index.html', ret_data)

    return render(request,'film/film_index.html',ret_data)


@login_required(login_url="/film/see/")
def vip(request,area):
    if area in ['xx','dxxg','xxx','xxxx']:

        ret_data = utils.DianYing(request, menu[area], role=area).page_info()
        return render(request, 'film/film_vip_index.html',ret_data)

    else:
        return render(request,'page_404.html')


def kankan(request,num):

    return render(request,'film/kankan.html',{'vip_film_url':'www.baidu.com'})



@login_required(login_url="/film/register/")
def vipkankan(request,role,num):
    vip_film_url='www.baidu.com'
    if num.isdigit() and role in ['xx','dxxg','xxx','xxxx']:
        for i in menu[role]:
            if int(num)==i[0]:
                vip_film_url=i[2]
        return render(request, 'film/kankan.html', {'vip_film_url': vip_film_url})
    else:

        return render(request,'page_404.html')



def film_logout(request):
    logout(request)
    return redirect('/film/see/')


def register(request):

    render(request,'page_403.html',{'errors':'注册会员后才能观看该影片'})


