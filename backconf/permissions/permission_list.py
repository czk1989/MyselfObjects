#!/usr/bin/env python
# -*- coding,utf-8 -*-
# _Auther_,Xiao Zhi
# Date,2018/11/5


perm_dic = {

    'can_get_index(king_admin)':['table_index', 'GET',[],{}],

    'can_get_table_objs(king_admin)':['table_objs','GET',[],{}],
    'can_post_table_objs(king_admin)':['table_objs','POST',[],{}],

    'can_get_edit_detail(king_admin)': ['edit_detail', 'GET', [], {}],
    'can_post_edit_detail(king_admin)': ['edit_detail','POST',[],{}],

    'can_get_change_pwd(king_admin)': ['change_pwd', 'GET', [], {}],
    'can_post_change_pwd(king_admin)': ['change_pwd', 'POST', [], {}],

    'can_get_obj_field_delete(king_admin)': ['obj_field_delete', 'GET', [], {}],
    'can_post_obj_field_delete(king_admin)': ['obj_field_delete', 'POST', [], {}],

    'can_get_obj_table_obj_add(king_admin)': ['table_obj_add', 'GET', [], {}],
    'can_post_obj_table_obj_add(king_admin)': ['table_obj_add', 'POST', [], {}],


    'can_get_index(crm)': ['crm_index', 'GET', [], {}],

    'can_get_customer(crm)': ['customers', 'GET', [], {}],

    'can_get_my_customers(crm)': ['my_customers', 'GET', [], {}],

    'can_get_customer_add(crm)': ['customer_add', 'GET', [], {}],
    'can_post_customer_add(crm)': ['customer_add', 'POST', [], {}],

    'can_get_my_customers_change(crm)': ['my_customers_change', 'GET', [], {},'crm_change_customer'],
    'can_post_my_customers_change(crm)': ['my_customers_change', 'POST', [], {},'crm_change_customer'],

    'can_get_customer_show(crm)': ['customer_show', 'GET', [], {}],



    'can_get_index(students)': ['stu_index', 'GET', [], {}],

    'can_get_stu_registered(students)': ['stu_registered', 'GET', [], {}],
    'can_post_stu_registered(students)': ['stu_registered', 'POST', [], {}],

    'can_get_jump(students)': ['jump', 'GET', [], {}],

    'can_get_classlist(students)': ['classlist', 'GET', [], {}],

    'can_get_my_course(students)': ['my_course', 'GET', [], {}],

    'can_get_payment(students)': ['payment', 'GET', [], {}],
    'can_post_payment(students)': ['payment', 'POST', [], {}],

    'can_get_pay(students)': ['pay', 'GET', [], {}],
    'can_post_pay(students)': ['pay', 'POST', [], {}],

    'can_get_enrollment(students)': ['enrollment', 'GET', [], {}],
    'can_post_enrollment(students)': ['enrollment', 'POST', [], {}],

    'can_get_studyrecord(students)': ['studyrecord', 'GET', [], {}],



    'can_get_index(teachers)': ['tea_index', 'GET', [], {}],

    'can_get_my_class(teachers)': ['my_class', 'GET', [], {}],

    'can_get_class_stu_list(teachers)': ['class_stu_list', 'GET', [], {},'limit_class_list_'],


}