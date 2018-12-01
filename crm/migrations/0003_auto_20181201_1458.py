# Generated by Django 2.1.3 on 2018-12-01 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20181201_0422'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('can_get_index(king_admin)', '可以访问 king_admin 首页02'), ('can_get_table_objs(king_admin)', '可以访问 king_admin 各个表02'), ('can_post_table_objs(king_admin)', '可以修改 king_admin 每个表中对象02'), ('can_get_edit_detail(king_admin)', '可以查看 king_admin 对应表详细信息02'), ('can_post_edit_detail(king_admin)', '可以修改 king_admin 对应表详细信息02'), ('can_get_change_pwd(king_admin)', '可以查看 king_admin 修改密码页面02'), ('can_post_change_pwd(king_admin)', '可以修改 king_admin 密码02'), ('can_get_obj_field_delete(king_admin)', '可以查看 king_admin 删除页面02'), ('can_post_obj_field_delete(king_admin)', '可以修改 king_admin 删除页面数据02'), ('can_get_obj_table_obj_add(king_admin)', '可以查看 king_admin 新增页面02'), ('can_post_obj_table_obj_add(king_admin)', '可以修改 king_admin 新增页面数据02'), ('can_get_index(crm)', '可以 访问 主页(crm)'), ('can_get_customer(crm)', '可以 访问 全部客户信息 页(crm)'), ('can_get_my_customers(crm)', '可以 访问 我的客户信息 页(crm)'), ('can_get_customer_add(crm)', '可以 访问 添加自己的客户信息 页(crm)'), ('can_post_customer_add(crm)', '可以 编辑 添加自己的客户信息 页(crm)'), ('can_get_my_customers_change(crm)', '可以 访问 修改自己的客户信息 页(crm)'), ('can_post_my_customers_change(crm)', '可以 编辑 修改自己的客户信息 页(crm)'), ('can_get_customer_show(crm)', '可以 访问 客户信息展示 页(crm)'), ('can_get_index(students)', '可以 访问 学生主页(students)'), ('can_get_stu_registered(students)', '可以 访问 账号注册 页(students)'), ('can_post_stu_registered(students)', '可以 编辑 账号注册 页(students)'), ('can_get_jump(students)', '可以 访问 账号注册成功跳转 页(students)'), ('can_get_classlist(students)', '可以 访问 全部班级信息 页(students)'), ('can_get_my_course(students)', '可以 访问 我的课程 页(students)'), ('can_get_payment(students)', '可以 访问 报名步骤2付款审核 页(students)'), ('can_post_payment(students)', '可以 编辑 报名步骤2付款审核 页(students)'), ('can_get_pay(students)', '可以 进入 报名步骤3付款确认 页(students)'), ('can_post_pay(students)', '可以 编辑 报名步骤3付款确认 页(students)'), ('can_get_enrollment(students)', '可以 进入 报名步骤1 页(students)'), ('can_post_enrollment(students)', '可以 编辑 报名步骤1 页(students)'), ('can_get_studyrecord(students)', '可以 访问 学习记录 页(students)'), ('can_get_index(teachers)', '可以 访问 讲师主页(teachers)'), ('can_get_my_class(teachers)', '可以 访问 我的课程 页(teachers)'), ('can_get_class_stu_list(teachers)', '可以 访问 学生学习记录 页(teachers)')), 'verbose_name_plural': 'CRM账户'},
        ),
    ]
