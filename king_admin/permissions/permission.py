#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/11/5
from king_admin.permissions import permission_list
from django.shortcuts import render,redirect
from MyselfObjects import settings
from django.urls import resolve,reverse #reverse相对变绝对，resolve绝对变相对


def perm_check(*args,**kwargs):
    request = args[0]
    resolve_url_obj = resolve(request.path)
    current_url_name = resolve_url_obj.url_name
    match_key = None
    match_results = [False, ]

    if request.user.is_authenticated is False:
         return 'no_login'
    for permission_key, permission_val in permission_list.perm_dic.items():

        per_url_name = permission_val[0]
        per_method = permission_val[1]
        perm_args = permission_val[2]
        perm_kwargs = permission_val[3]
        custom_perm_func = None if len(permission_val) == 4 else permission_val[-1]

        if per_url_name == current_url_name:
            if per_method == request.method:
                # 逐个匹配参数，看每个参数时候都能对应的上。
                args_matched = False  # for args only
                for item in perm_args:
                    request_method_func = getattr(request, per_method)
                    if request_method_func.get(item, None):  # request字典中有此参数
                        args_matched = True
                    else:
                        args_matched = False
                        break  # 有一个参数不能匹配成功，则判定为假，退出该循环。
                else:
                    args_matched = True


                # 匹配有特定值的参数
                kwargs_matched = False
                for k, v in perm_kwargs.items():
                    request_method_func = getattr(request, per_method)
                    arg_val = request_method_func.get(k, None)  # request字典中有此参数
                    if arg_val == str(v):  # 匹配上了特定的参数 及对应的 参数值， 比如，需要request 对象里必须有一个叫 user_id=3的参数
                        kwargs_matched = True
                    else:
                        kwargs_matched = False
                        break  # 有一个参数不能匹配成功，则判定为假，退出该循环。
                else:
                    kwargs_matched = True

                # 自定义权限钩子
                perm_func_matched = False
                if custom_perm_func:
                    if custom_perm_func(request, args, kwargs):
                        perm_func_matched = True
                    else:
                        perm_func_matched = False  # 使整条权限失效

                else:  # 没有定义权限钩子，所以默认通过
                    perm_func_matched = True

                match_results = [args_matched, kwargs_matched, perm_func_matched]
                if all(match_results):  # 都匹配上了
                    match_key = permission_key
                    break

    if all(match_results):

        perm_obj = match_key
        if request.user.has_perm(perm_obj):
            # print('111当前用户有此权限')
            # print(dir(request.user.get_all_permissions))
            # print(request.user.get_all_permissions)
            return True
        else:
            # print('222当前用户没有该权限')
            return False
    else:
        # print("未匹配到权限项，当前用户无权限")
        pass


def check_permission(func):
    def inner(*args, **kwargs):
        result = perm_check(*args, **kwargs)
        if result == 'no_login':
            return redirect(settings.LOGIN_URL)
        if not result:
            request = args[0]
            return render(request,'king_admin/page_403.html')
        return func(*args, **kwargs)
    return inner