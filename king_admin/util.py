#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/10/24
# models.Customer.objects.filter()
from django.db import models
from django.db.models import Q

#条件筛选功能
def table_utils(request,admin_class):
    key_word=['page','o','_q','csrfmiddlewaretoken']
    filter_condition={}
    for k,v in request.GET.items():
        if k in key_word:       #保留的分页关键字和排序关键字
            continue
        if v:
            filter_condition[k]=v
    return admin_class.models.objects.filter(**filter_condition).\
               order_by("%s"%admin_class.ordering if admin_class.ordering else '-id'),\
               filter_condition


#排序功能函数
def table_order(request,objs):
    orderby_key=request.GET.get('o')

    if orderby_key:
        res=objs.order_by(orderby_key)
        if orderby_key.startswith('-'):
            orderby_key=orderby_key.strip('-')
        else:
            orderby_key='-%s'%orderby_key
    else:
        res=objs
    return res,orderby_key

#搜索功能
def table_search(request,object_list,admin_class):
    search_info=request.GET.get('_q','')
    q_obj=Q()
    q_obj.connector="OR"

    for column in admin_class.list_search:
        q_obj.children.append(("%s__contains"%column,search_info))

    res=object_list.filter(q_obj)
    return res,search_info