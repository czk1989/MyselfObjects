
from django.shortcuts import render,redirect
from django.shortcuts import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from crm import models
from king_admin import views_base
from king_admin import king_admin_base
from king_admin import util
from backconf.permissions.permission import check_permission

@login_required(login_url="/accounts/crm/login/")
@check_permission
def sales_index(request):
    if request.user.roles.first().name=='manager':
        return redirect('/king_admin/')
    menus=views_base.MenuList(request).shoumenus()
    return render(request, 'crm/sales_index.html', {'menus':menus})



@login_required(login_url="/accounts/crm/login/")
@check_permission
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
@check_permission
def customer_show(request,table_name,customer_num):
    return_data=views_base.TableChange(request, 'crm', table_name, customer_num,embed=False,edit=False).edittable()
    if type(return_data) is dict:
        return render(request, 'crm/customer_show.html', return_data)
    else:
        return return_data


@login_required(login_url="/accounts/crm/login/")
@check_permission
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
@check_permission
def my_customers_change(request,num):
    return_data=views_base.TableChange(request, 'crm', 'customer', num,embed=False,edit=True).edittable()
    if type(return_data) is dict:
        return render(request, 'crm/my_customers_change.html', return_data)
    else:
        return return_data

@login_required(login_url="/accounts/crm/login/")
@check_permission
def my_customers_add(request):
    return_data=views_base.DataAdd(request,'crm','customer',embed=False).add_data()
    if type(return_data) is dict:
        return render(request, 'crm/my_customers_add.html', return_data)
    else:
        return return_data


