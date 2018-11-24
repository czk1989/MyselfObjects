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
def course_title(column,list_display):
    res=''
    title='<th>{title}</th>'
    for i in list_display:

        if i == 'id':
            res += title.format(title='序号')
            continue
        b = column._meta.get_field(i)
        if hasattr(b,'verbose_name'):
            res+=title.format(title=b.verbose_name)
        else:
            res+=title.format(title=b)
    res+=title.format(title='报名入口')
    return mark_safe(res)


# 内容
@register.simple_tag
def built_table_row(obj,list_display,stu_enroll_dict):
    ret=''
    for index,column in enumerate(list_display):
        #下面代码判断是否为choices，如果是，就取到对应的字符，而不是序列化的id号
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:
            column_data=getattr(obj,'get_%s_display'%column)()
        else:
            column_data = getattr(obj, column)
            if type(column_data).__name__=='datetime':
                column_data=column_data.strftime('%Y-%m-%d %H:%M:%S')

        ret+='<td>%s</td>'%column_data

    # 判断用户是否已经报了该课程，如果报过名，默认不再显示报名连接
    if obj in stu_enroll_dict:
        if stu_enroll_dict[obj].contract_approved:
            ret += "<td>已报过名</td>"
        else:
            ret += "<td><a href='/students/pay/%s/' style='color:red'>付款</a></td>" % stu_enroll_dict[obj].id
    else:
        ret += "<td><a href='/students/enrollment/%s/'>报名</a></td>" % obj.id
    return mark_safe(ret)


@register.simple_tag
def stu_class(stu_classlist):
    ret=""
    a="<div class='row'><label class='form-group'>{branch}/{course}/第{semester}学期</label></div>"
    if len(stu_classlist)>0:
        for myclass in stu_classlist:
            ret+=a.format(branch=myclass.branch,course=myclass.course,semester=myclass.semester)
    else:
        ret="<div class='row'><label class='form-group'>暂无课程，请在班级表中选择新课程报名...</label></div>"
    return mark_safe(ret)