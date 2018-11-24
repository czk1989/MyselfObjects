#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/10/22

from django.shortcuts import render

from django import conf


class BaseAdmin(object):
    list_display=[]
    list_filters=[]
    list_per_page=20
    list_search=[]
    ordering='-id'
    filter_horizontal = ['tag']
    list_action = ['delete_choice_fields']
    readonly_fields=[]
    fk_fields=[]
    list_editable = []
    readonly_table = False
    modelform_exclude_fields = []
    # search_fields=[]
    colored_field={}
    add_form = None
# action功能函数
    def delete_choice_fields(self,request,querysets,menus):
        objs_id=''
        for obj in querysets:
            objs_id+=str(obj.id)
            objs_id+=','
        return render(request, 'king_admin/king_admin_table_objs_delete.html', {'objs':querysets,
                                                                    'admin_class':self,
                                                                    'app_name':self.models._meta.app_label,
                                                                    'table_name':self.models._meta.model_name,
                                                                   'objs_id': objs_id,
                                                                   'menus': menus,
                                                                                })

    delete_choice_fields.display_name='删除表单数据'

#这里可以写用户自定义的clean方法，用来进行表单验证
    def default_form_validation(self):
        pass


class AdminAlreadyRegistered(Exception):
    def __init__(self,msg):
        self.message = msg


class KingAdminSite(object):
    def __init__(self):
        self.enabled_admin = {}

    def register(self,model_class,admin_class=None):
        if model_class._meta.app_label not in self.enabled_admin:
            self.enabled_admin[model_class._meta.app_label] = {}

        if not admin_class:
            admin_class = BaseAdmin()
        admin_class.models = model_class
        self.enabled_admin[model_class._meta.app_label][model_class._meta.model_name] = admin_class
site= KingAdminSite()

for app in conf.settings.INSTALLED_APPS:
    try:
        admin_module = __import__("%s.king_admin" % app)
    except ImportError:
        pass

