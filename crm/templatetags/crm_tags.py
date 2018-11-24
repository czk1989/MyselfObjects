#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/10/22
from django import template
from king_admin import tag_base
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist

register=template.Library()

@register.simple_tag
def render_enroll_contract(enroll_obj):
    return enroll_obj.enrolled_class.contract.template.format(enroll_tontract=enroll_obj.customer.qq)
#
@register.simple_tag
def render_app_name(admin_class):
    return tag_base.render_app_name(admin_class)

@register.simple_tag
def get_key_val(condition,admin_class):
    return tag_base.get_key_val(condition,admin_class)


@register.simple_tag
def search_name(condition, admin_class):
    return tag_base.search_name(condition, admin_class)

@register.simple_tag
def render_filter_eme(condition,admin_class,filter_condition):
    return tag_base.render_filter_eme(condition,admin_class,filter_condition)

@register.simple_tag
def func_name(func_list, admin_class):
    return tag_base.func_name(func_list, admin_class)

@register.simple_tag
def buile_table_header_column(admin_class,column,orderby_key,filter_condition):
    return tag_base.buile_table_header_column(admin_class,column,orderby_key,filter_condition)


#显示数据库表需要列出来的详细信息
@register.simple_tag
def show_table(obj,admin_class,request):
    ret=''
    for index,column in enumerate(admin_class.list_display):

        #下面代码判断是否为choices，如果是，就取到对应的字符，而不是序列化的id号
        try:
            field_obj = obj._meta.get_field(column)
            if field_obj.choices:
                column_data=getattr(obj,'get_%s_display'%column)()
            else:
                column_data = getattr(obj, column)
            if column=='groups':
                if hasattr(obj,'groups'):
                    if hasattr(obj.groups,'name'):
                        column_data=obj.groups.first().name
            if type(column_data).__name__=='datetime':
                column_data=column_data.strftime('%Y-%m-%d %H:%M:%S')
            if index==0:
                ret+='<td><a href="%s%s/show/">%s</a></td>'%(request.path,column_data,column_data)
            else:
               ret+='<td>%s</td>'%column_data

# 判断显示列表的元素如果不在数据库表，那么可能在king_admin定义类的时候声明了对应名称的函数
        except FieldDoesNotExist as e:
            if hasattr(admin_class,column):
                column_func=getattr(admin_class,column)
                admin_class.instance=obj
                admin_class.request=request
                column_data=column_func()
                ret+='<td>%s</td>'%column_data
    return mark_safe(ret)


@register.simple_tag
def built_table_row(obj,admin_class,request):
    return tag_base.built_table_row(obj,admin_class,request)

#实现分页按钮
@register.simple_tag
def page_index(query_sets,filter_condition,previous_orderby,search_key):
    return tag_base.page_index(query_sets,filter_condition,previous_orderby,search_key)

#返回m2m所有传递数据
@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    return tag_base.get_m2m_obj_list(admin_class,field,form_obj)

@register.simple_tag
def get_choiced_field(form_obj,foo):
    return tag_base.get_choiced_field(form_obj,foo)

@register.simple_tag
def delete_field_obj(form_obj,delete_url_path):
    return tag_base.delete_field_obj(form_obj,delete_url_path)

#显示要删除的详细信息的功能暂未开发
@register.simple_tag
def display_obj_related(objs,tabel_name):
    return tag_base.display_obj_related(objs,tabel_name)

@register.simple_tag
def to_url(objs,app_name,tabel_name):
    return tag_base.to_url(objs,app_name,tabel_name)