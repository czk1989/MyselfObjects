from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
import uuid,os,shutil
from MyselfObjects import settings
from backconf import verification,redis_cli

REDIS_CONN=redis_cli.redis_conn()

def login_choice(request):

    return render(request,'login_choice.html')

def sys_login(request,app_name):
    file_name = str(uuid.uuid4())
    shutil.rmtree(settings.VERIFICATION_CODE_IMGS_DIR)
    os.mkdir(settings.VERIFICATION_CODE_IMGS_DIR)
    random_code = verification.gene_code(settings.VERIFICATION_CODE_IMGS_DIR, file_name)
    REDIS_CONN.set(file_name, random_code, settings.REDIS_TIMEOUT_VERIF)
    errors = {}
    if request.method == "POST":
        app_url={'students': 'students', 'king_admin': 'manager', 'crm': 'sales', 'teachers': 'teachers'}
        if app_name in app_url:
            _name = request.POST.get('email','email')
            _password = request.POST.get('password','pwd')
            _verify_code = request.POST.get('verify_code','no')
            _verify_code_key = request.POST.get('verify_code_key','no')
            if REDIS_CONN.get(_verify_code_key).upper() == bytes(_verify_code.upper(),encoding='utf-8'):
                user = authenticate(username=_name, password=_password)
                if user and user.roles.first().name==app_url[app_name]:
                    login(request, user)
                    # request.session.set_expiry(60 * 600)
                    return HttpResponseRedirect(request.GET.get("next") if request.GET.get("next") else "/%s/" % app_name)
                else:
                    errors = '账号或密码错误，请重新输入'
            else:
                errors= '验证码错误'
        else:
            errors = '谢谢你能来到这里...'
            return render(request, 'page_403.html', {'errors': errors})
    return render(request, 'login.html', {'errors': errors,
                                          "filename": file_name,
                                          'app_name':app_name,
                                          })


def sys_logout(request):
    logout(request)
    return redirect('/accounts/')

def myobjects(request):

    return render(request, 'index.html')


