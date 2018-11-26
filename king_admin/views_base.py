
from django.shortcuts import HttpResponseRedirect, render,redirect
from django.contrib.auth import login,authenticate
from django.core.cache import cache
from django.core.paginator import Paginator
from king_admin import king_admin_base
from king_admin import util
from crm import models
from king_admin import forms

class MenuList(object):
    def __init__(self,request):
        self.request=request

    def shoumenus(self):
        menus={}
        try:
            firstmenus=models.UserProfile.objects.filter(email=self.request.user.email).first().roles.first().menus.all()
            for firstmenu in firstmenus:
                menus[firstmenu]=firstmenu.sub_menus.all()
            return menus
        except Exception as e:
            return None
    def adminmenus(self):
        table_list=king_admin_base.site.enabled_admin
        menus={}
        print(len(menus))
        tablemenus={}
        for app_name,table_objs in table_list.items():
            for k,admin in table_objs.items():
                table_name=admin.models._meta.verbose_name_plural
                table_url=admin.models._meta.model_name
                tablemenus[table_name]=table_url
            menus[app_name]=tablemenus
            tablemenus={}
        print(len(menus))
        if len(menus) < 1:
            return False
        else:
            return menus


class TableDisplay(object):
    def __init__(self, request, app_name, table_name,embed):
        self.request = request
        self.app_name = app_name
        self.table_name = table_name
        self.embed=embed

    def show_table(self):
        if self.app_name in king_admin_base.site.enabled_admin:
            if self.table_name in king_admin_base.site.enabled_admin[self.app_name]:
                admin_class = king_admin_base.site.enabled_admin[self.app_name][self.table_name]
                object_list, filter_condition = util.table_utils(self.request, admin_class)
                object_list, orderby_key = util.table_order(self.request, object_list)
                object_list, search_key = util.table_search(self.request, object_list, admin_class)
                if self.embed:
                    menus=MenuList(self.request).adminmenus()
                else:
                    menus=MenuList(self.request).shoumenus()
                if self.request.method == 'POST':
                    selected_ids = self.request.POST.get('selected_list')
                    action = self.request.POST.get('action')
                    if selected_ids:
                        selected_objs = admin_class.models.objects.filter(id__in=selected_ids.split(','))
                    else:
                        raise KeyError('No object selected')
                    if hasattr(admin_class, action):
                        action_func = getattr(admin_class, action)
                        return action_func(admin_class, self.request, selected_objs, menus)
                paginator = Paginator(object_list, 5)  # Show 25 contacts per page
                page = self.request.GET.get('page')
                query_sets = paginator.get_page(page)
                data = {'admin_class': admin_class,
                        'query_sets': query_sets,
                        'filter_condition': filter_condition,
                        'orderby_key': orderby_key,
                        'previous_orderby': self.request.GET.get('o', ''),
                        'search_key': search_key,
                        'menus': menus,
                        'app_name': self.app_name,
                        'table_name': self.table_name,
                        }

                return data

        else:
            return False

class Login(object):
    def __init__(self,request,app_name,role):
        self.request=request
        self.app_name=app_name
        self.role=role

    def acc_login(self):
        errors={}
        if self.request.method == "POST":
            _name=self.request.POST.get('email')
            _password=self.request.POST.get('password')
            #_verify_code和_verify_code_key暂时还未设置，为None
            _verify_code = self.request.POST.get('verify_code')
            _verify_code_key=self.request.POST.get('verify_code_key')
            if cache.get(_verify_code_key) == _verify_code:
                user = authenticate(username=_name, password=_password)
                if user:
                    login(self.request,user)
                    # request.session.set_expiry(60 * 600)
                    return HttpResponseRedirect(self.request.GET.get("next") if self.request.GET.get("next") else "/%s/"%self.app_name)
                else:
                    errors['error']='Wrong user or password'
            else:
                errors['error'] = '验证码错误'
        return render(self.request, '%s/login.html'%self.app_name, {'errors':errors,'role':self.role})


class TableChange(object):
    def __init__(self,request, app_name, table_name, num,embed,edit):
        self.request=request
        self.app_name=app_name
        self.table_name=table_name
        self.num=num
        self.embed=embed
        self.edit=edit
    def edittable(self):
        admin_class=king_admin_base.site.enabled_admin[self.app_name][self.table_name]
        admin_class.read_only = True
        if self.edit:
            model_form_class = forms.create_modelform(self.request, admin_class)
        else:
            model_form_class = forms.show_modelform(self.request, admin_class)
        change_table_data = admin_class.models.objects.get(id=self.num)
        delete_url_path = self.request.path.replace('/change/', '/delete/')

        form_obj = model_form_class(instance=change_table_data)
        if self.embed:
            menus=MenuList(self.request).adminmenus()
        else:
            menus=MenuList(self.request).shoumenus()
        if self.request.method == 'POST':
            form_obj = model_form_class(self.request.POST, instance=change_table_data)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(self.request.path.replace('/%s/change/' % self.num, '/'))

        data={'form_obj': form_obj,
                'admin_class': admin_class,
                'delete_url_path': delete_url_path,
                'menus':menus,
                'app_name': self.app_name,
                'table_name': self.table_name
                }
        return data

    def showtable(self):
        pass


class DataAdd(object):
    def __init__(self,request,app_name,table_name,embed):
        self.request=request
        self.app_name=app_name
        self.table_name=table_name
        self.embed=embed

    def add_data(self):
        admin_class = king_admin_base.site.enabled_admin[self.app_name][self.table_name]
        admin_class.read_only = False
        model_form_class = forms.create_modelform(self.request, admin_class)
        if self.embed is True:
            menus=MenuList(self.request).adminmenus()
        elif self.embed is False:
            menus=MenuList(self.request).shoumenus()
        else:
            menus=''
        if self.request.method == 'POST':
            form_obj = model_form_class(self.request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(self.request.path.replace('/add/', '/'))
        else:
            form_obj = model_form_class()

        data={'form_obj': form_obj,
             'admin_class': admin_class,
             'menus':menus,
             'app_name': self.app_name,
             'table_name': self.table_name,
              }
        return data


class CreatAccount(object):
    def __init__(self,request,is_staff,role):
        self.request=request
        self.is_staff=is_staff
        self.role=role

    def redigtered(self):
        errors = ''
        account_form = forms.UserProfileForm()
        account_obj = account_form
        if self.request.method == 'POST':
            account_obj = forms.UserProfileForm(self.request.POST)
            if account_obj.is_valid():
                account_obj.save()
                account_fin = models.UserProfile.objects.filter(email=account_obj.instance.email).first()
                account_fin.is_staff = self.is_staff
                account_fin.roles.add(models.Role.objects.filter(name=self.role).first())
                account_fin.save()
                if not models.Customer.objects.filter(email=account_obj.instance.email).first():
                    models.Customer.objects.create(name=account_obj.instance.name,email=account_obj.instance.email,)
                customer_data=models.Customer.objects.get(email=account_obj.instance.email)
                user_data=account_fin
                return_list=[user_data,customer_data]
                return return_list
            else:
                errors = '该账号已被注册，请重新输入email...'
        data = {'account_obj': account_obj,
                'app_name': 'crm',
                'table_name': 'userprofile',
                'errors': errors,
                }
        return data
