#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/10/22
from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta

register=template.Library()
from king_admin import tag_base

#返回App的名称
@register.simple_tag
def render_app_name(admin_class):
    # return admin_class.models._meta.verbose_name_plural
    return tag_base.render_app_name(admin_class)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.models._meta.verbose_name_plural


@register.simple_tag
def search_name(condition,admin_class):
    # if hasattr(admin_class.models,condition):
    #     return admin_class.models._meta.get_field(condition).verbose_name
    # else:
    #     k,v=condition.split('__')
    #     if hasattr(admin_class.models,k) and hasattr(admin_class.models._meta.get_field(k),'related_model'):
    #         return admin_class.models._meta.get_field(k).related_model._meta.get_field(v).verbose_name
    #     else:
    #         return condition

    return tag_base.search_name(condition,admin_class)


@register.simple_tag
def get_key_val(condition,admin_class):
    # if hasattr(admin_class.models,str(condition)):
    #     return admin_class.models._meta.get_field(condition).verbose_name
    # else:
    #     return condition
    return tag_base.get_key_val(condition,admin_class)

#显示数据库表需要列出来的详细信息
@register.simple_tag
def built_table_row(obj,admin_class,request):
#     ret=''
#     for index,column in enumerate(admin_class.list_display):
#
#         #下面代码判断是否为choices，如果是，就取到对应的字符，而不是序列化的id号
#         try:
#             field_obj = obj._meta.get_field(column)
#             if field_obj.choices:
#                 column_data=getattr(obj,'get_%s_display'%column)()
#             else:
#                 column_data = getattr(obj, column)
#             if column=='groups':
#                 if hasattr(obj,'groups'):
#                     if hasattr(obj.groups,'name'):
#                         column_data=obj.groups.first().name
#             if type(column_data).__name__=='datetime':
#                 column_data=column_data.strftime('%Y-%m-%d %H:%M:%S')
#             if index==0:
#                 ret+='<td><a href="%s%s/change/">%s</a></td>'%(request.path,column_data,column_data)
#             else:
#                ret+='<td>%s</td>'%column_data
#
# # 判断显示列表的元素如果不在数据库表，那么可能在king_admin定义类的时候声明了对应名称的函数
#         except FieldDoesNotExist as e:
#             if hasattr(admin_class,column):
#                 column_func=getattr(admin_class,column)
#                 admin_class.instance=obj
#                 admin_class.request=request
#                 column_data=column_func()
#                 ret+='<td>%s</td>'%column_data
#     return mark_safe(ret)
    return tag_base.built_table_row(obj,admin_class,request)

#实现分页按钮
@register.simple_tag
def page_index(query_sets,filter_condition,previous_orderby,search_key):
    # ret=''
    # page_num=1
    # start=query_sets.number-page_num
    # last=query_sets.number+page_num
    # count = query_sets.paginator.num_pages
    # last_table = ''
    # page_info=''
    # add_info='&o=%s&_q=%s'%(previous_orderby,search_key)
    # for k, v in filter_condition.items():
    #     page_info += '&%s=%s' % (k, v)
    # if count>1:
    #     if start>1:
    #         ret+='<li class=""><a href="?page=1%s%s">&laquo;首页</a></li>'%(page_info,add_info)
    #     else:
    #         start=1
    #     if query_sets.number>1:
    #         ret += '<li class =""><a href="?page=%s%s%s">上一页</ a> </li>' %(query_sets.number-1,page_info,add_info)
    #     if last<count :
    #         last_table='<li class=""><a href="?page=%s%s%s">最后一页 &raquo;</a></li>'%(query_sets.paginator.num_pages,page_info,add_info)
    #     else:
    #         last=count
    #     for i in range(start,last+1):
    #         if i==query_sets.number:
    #             ret+='<li class ="active"><a href="?page=%s%s%s">%s</a></li>'%(i,page_info,add_info,i)
    #         else:
    #             ret+='<li><a href="?page=%s%s%s">%s</a></li>'%(i,page_info,add_info,i)
    #     if query_sets.number <count:
    #         ret+='<li class=""><a href="?page=%s%s%s">下一页</a></li>'%(query_sets.number+1,page_info,add_info)
    #     ret+=last_table
    #     # return mark_safe(ret)
    # else:
    #     ret += '<li class ="active"><a href="?page=%s%s">1</a></li>'%(query_sets.number,page_info)
    # return mark_safe(ret)
    return tag_base.page_index(query_sets,filter_condition,previous_orderby,search_key)

#返回需要查询的条件
@register.simple_tag
def render_filter_eme(condition,admin_class,filter_condition):
    # # condition_name='%s__gte'%condition
    # # select_eme="<select class='form-control' name='%s'><option value=''>-------</option>"%condition
    # select_eme="<select class='form-group btn-sm' name='{filter_name}'><option value=''>--------</option>"
    # # select_eme.format(condition=condition)
    # field_obj=admin_class.models._meta.get_field(condition)
    # if field_obj.choices:
    #     selected=' '
    #     for choice_item in field_obj.choices:
    #         if filter_condition.get(condition)==str(choice_item[0]):
    #             selected='selected'
    #         select_eme+="<option value='%s' %s>%s</option>"%(choice_item[0],selected,choice_item[1])
    #         selected = ' '
    #         # select_eme+="<option value='%s'>%s</option>"%(choice_item[0],choice_item[1])
    # if type(field_obj).__name__=='ForeignKey':
    #     selected=''
    #     for choice_item in field_obj.get_choices()[1:]:
    #         if filter_condition.get(condition)==str(choice_item[0]):
    #             selected='selected'
    #
    #         select_eme+="<option value='%s' %s>%s</option>"%(choice_item[0],selected,choice_item[1])
    #         selected = ' '
    # if type(field_obj).__name__ == 'ManyToManyField':
    #     selected = ''
    #     for choice_item in field_obj.get_choices()[1:]:
    #         if filter_condition.get(condition) == str(choice_item[0]):
    #             selected = 'selected'
    #         select_eme += "<option value='%s' %s>%s</option>" % (choice_item[0], selected, choice_item[1])
    #         selected = ' '
    #
    # if type(field_obj).__name__ in ['DateTimeField','DateField']:
    #     date_ele=[]
    #     today_ele=datetime.now().date()
    #     date_ele.append(['今天',datetime.now().date()])
    #     date_ele.append(['昨天',today_ele-timedelta(days=1)])
    #     date_ele.append(['近7天',today_ele-timedelta(days=7)])
    #     date_ele.append(['本月',today_ele.replace(day=1)])
    #     date_ele.append(['近30天',today_ele-timedelta(days=30)])
    #     date_ele.append(['近3个月',today_ele-timedelta(days=90)])
    #     date_ele.append(['近6个月',today_ele-timedelta(days=180)])
    #     date_ele.append(['本年',today_ele.replace(month=1,day=1)])
    #     date_ele.append(['近一年',today_ele-timedelta(days=365)])
    #
    #     selected = ''
    #     for choice_item in date_ele:
    #         find_condition='%s__gte'%condition
    #         if filter_condition.get(find_condition)==str(choice_item[1]):
    #             selected='selected'
    #         select_eme += "<option value='%s' %s>%s</option>" % (choice_item[1], selected, choice_item[0])
    #         selected = ' '
    #     filter_name='%s__gte'%condition
    # else:
    #     filter_name=condition
    #
    # select_eme+="</select>"
    # select_eme=select_eme.format(filter_name=filter_name)
    return tag_base.render_filter_eme(condition,admin_class,filter_condition)


@register.simple_tag
def buile_table_header_column(admin_class,column,orderby_key,filter_condition):
    # if column!='enroll':
    #     ele = "<a href='?{filter_condition}o={orderby_key}'>{column_name}</a>{img}"
    #     x=''
    #     for k,v in filter_condition.items():
    #         x+='%s=%s&'%(k,v)
    #
    #     img=''
    #     if orderby_key:
    #         if orderby_key.strip('-')==column:
    #             orderby_key=orderby_key
    #             if orderby_key.startswith('-'):
    #                 img='<span class="glyphicon glyphicon-arrow-up" aria-hidden="true"></span>'
    #             else:
    #                 img = '<span class="glyphicon glyphicon-arrow-down" aria-hidden="true"></span>'
    #         else:
    #             orderby_key=column
    #     else:
    #         img=''
    #         orderby_key=column
    #     if hasattr(admin_class.models,str(column)):
    #         column_name= admin_class.models._meta.get_field(column).verbose_name
    #     else:
    #         column_name=column
    #     if column=='id':
    #         column_name='序号'
    #     ele=ele.format(filter_condition=x,orderby_key=orderby_key,column_name=column_name,img=img)
    #     return mark_safe(ele)
    # else:
    #     column='报名入口'
    #     return mark_safe('<span>%s</span>'%column)
    return tag_base.buile_table_header_column(admin_class,column,orderby_key,filter_condition)

#返回m2m所有传递数据
@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    # class_name=getattr(admin_class.models,field.name)
    # #表结构对象的某个字段
    # all_obj_list=class_name.rel.model.objects.all()
    #
    # #去除已经被选中的字段
    # if form_obj.instance.id:
    #     obj_instance_field=getattr(form_obj.instance,field.name)
    #     selected_obj_list=obj_instance_field.all()
    # else:
    #     return all_obj_list
    # standby_obj_list=[]
    # for obj in all_obj_list:
    #     if obj not in selected_obj_list:
    #         standby_obj_list.append(obj)
    # return standby_obj_list
    return tag_base.get_m2m_obj_list(admin_class,field,form_obj)

@register.simple_tag
def get_choiced_field(form_obj,foo):
    # name=foo.name
    # choiced_field=''
    # if form_obj.instance.id:
    #     x=getattr(form_obj.instance,name)
    #     choiced_field=x.all()
    # return choiced_field
    return tag_base.get_choiced_field(form_obj,foo)


@register.simple_tag
def delete_field_obj(form_obj,delete_url_path):
    # if form_obj.instance.id:
    #     return mark_safe("<a href='%s'><span class ='glyphicon glyphicon-trash btn ' aria-hidden='true'>删除</span></a>"%delete_url_path)
    #
    # else:
    #     return ''
    return tag_base.delete_field_obj(form_obj,delete_url_path)

#显示要删除的详细信息的功能暂未开发
@register.simple_tag
def display_obj_related(objs,tabel_name):
    # ele=''
    # if hasattr(objs,'values_list'):
    #     for obj in objs:
    #         ele+='<ul><h4>表单：%s</h4><li>数据记录：%s</li></ul>'%(tabel_name,obj.id)
    # else:
    #     ele+='<ul><h4>表单：%s</h4><li>数据记录：%s</li></ul>'%(tabel_name,objs.id)
    # return mark_safe(ele)
    return tag_base.display_obj_related(objs,tabel_name)

@register.simple_tag
def to_url(objs,app_name,tabel_name):
    # if hasattr(objs, 'values_list'):
    #     url_choice='/king_admin/%s/%s/all/delete/'%(app_name,tabel_name)
    # else:
    #     url_choice='/king_admin/%s/%s/%s/delete/'%(app_name,tabel_name,objs.id)
    # return url_choice
    return tag_base.to_url(objs,app_name,tabel_name)

# 显示action的中文名
@register.simple_tag
def func_name(func_list, admin_class):
    # if hasattr(admin_class,func_list):
    #     func=getattr(admin_class,func_list)
    #     return func.display_name
    # else:
    #     return func_list

    return tag_base.func_name(func_list, admin_class)