

from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser
from django.utils.safestring import mark_safe
from django.contrib.auth.models import PermissionsMixin
from crm import auth
from django.utils.translation import ugettext_lazy as _

# 3客户表
class Customer(models.Model):
    name=models.CharField(max_length=32,blank=True,null=True,verbose_name='姓名')
    qq=models.CharField(max_length=64,blank=True,null=True,unique=True)
    qq_name=models.CharField(max_length=64,blank=True,null=True,verbose_name='QQ昵称')
    phone=models.CharField(max_length=64,blank=True,null=True,verbose_name='联系电话')
    source_choices=(
        (0,'转介绍'),
        (1,'QQ群'),
        (2,'官网'),
        (3,'百度推广'),
        (4,'51CTO'),
        (5,'知乎'),
        (6,'市场推广'),)
    source=models.SmallIntegerField(choices=source_choices,verbose_name='客户来源',default=0)
    referral_from=models.ForeignKey('self',verbose_name="转介绍人",help_text=u"若介绍人是内部学员,请在此处选择内部学员姓名",blank=True,null=True,related_name="internal_referral",on_delete=models.CASCADE)
    consult_course=models.ForeignKey('Course',blank=True,null=True,verbose_name='咨询课程',on_delete=None)
    content=models.TextField(verbose_name='咨询详情')
    id_num=models.CharField(max_length=64,verbose_name='身份证',blank=True,null=True)
    email=models.EmailField(verbose_name='常用邮箱',blank=True,null=True,unique=True)
    consultant=models.ForeignKey('UserProfile',verbose_name='跟进人',blank=True,null=True,on_delete=None)
    date=models.DateTimeField(auto_now_add=True,verbose_name='日期')
    tag=models.ManyToManyField("Tag",blank=True,null=True,default=None,verbose_name='职业状态')
    status_choices=((0,'未报名'),
                    (1,'已报名'))
    status=models.SmallIntegerField(choices=status_choices,default=0,verbose_name='报名情况')

    def __str__(self):
        return '姓名:%s'%(self.email)
    class Meta:
        verbose_name_plural='客户信息表'

    def clean_status(self):
        status = self.cleaned_data['status']
        if self.instance.id == None:  # add form
            if status == 0:
                raise forms.ValidationError(("必须走完报名流程后，此字段才能改名已报名"))
            else:
                return status

        else:
            return status

    def clean_consultant(self):
        consultant = self.cleaned_data['consultant']

        if self.instance.id == None :#add form
            return self._request.user

        elif consultant.id != self.instance.consultant.id:
            raise forms.ValidationError(('Invalid value: %(value)s 课程顾问不允许被修改,shoud be %(old_value)s'),
                                         code='invalid',
                                         params={'value': consultant,'old_value':self.instance.consultant})
        else:
            return consultant

# 4标签表
class Tag(models.Model):
    name=models.CharField(unique=True,max_length=32,verbose_name='头衔')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='职业状态'


# 5客户跟进表
class CustomerFollowUp(models.Model):
    '''客户跟进表'''
    customer=models.ForeignKey('Customer',blank=True,null=True,on_delete=None,verbose_name='咨询客户跟踪')
    content=models.TextField(verbose_name='跟进内容')
    consultant=models.ForeignKey("UserProfile",blank=True,null=True,on_delete=None,verbose_name='跟进人')
    intention_choices=((0,'2周内报名'),
                       (1,'1个月内报名'),
                       (2,'近期无报名计划'),
                       (3,'已在其他机构报名'),
                       (4,'未报名'),
                       (5,'已报名'),
                       (6,'已拉黑'),)
    intention=models.SmallIntegerField(choices=intention_choices,verbose_name='跟踪情况')
    date=models.DateTimeField(auto_now_add=True,verbose_name='时间')

    def __str__(self):
        return '%s:%s'%(self.customer.name,self.intention)
    class Meta:
        verbose_name_plural='客户跟进记录'

# 6课程表
class Course(models.Model):
    '''课程表'''
    name=models.CharField(max_length=64,unique=True,verbose_name='课程名')
    description = models.TextField("课程描述")
    period=models.PositiveSmallIntegerField(verbose_name='周期(月)')
    outline=models.TextField("课程描述")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='课程表'


# 7校区表
class Branch(models.Model):
    '''校区'''
    name=models.CharField(max_length=128,unique=True,verbose_name='校区')
    addr=models.CharField(max_length=128,verbose_name='地址')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='校区表'


# 8班级表
class ClassList(models.Model):
    '''班级表'''
    branch=models.ForeignKey('Branch',blank=True,null=True,verbose_name='校区',on_delete=None)
    course=models.ForeignKey('Course',blank=True,null=True,on_delete=None,verbose_name='课程')
    contract=models.ForeignKey('ContractTemplate',blank=True,null=True,on_delete=None,verbose_name='合同')
    class_type_choices=(
        (0,'面授(脱产)'),
        (1,'面授(周末)'),
        (2,'网络班'),
    )
    class_type=models.SmallIntegerField(choices=class_type_choices,verbose_name='班级类型')
    total_class_nums = models.PositiveIntegerField("课程总节次", default=10)
    semester=models.PositiveSmallIntegerField(verbose_name='学期')
    price = models.IntegerField(u"学费", default=5000)
    teachers=models.ManyToManyField('UserProfile',blank=True,null=True,verbose_name='上课讲师')
    start_date=models.DateField(verbose_name='开班日期')
    end_date=models.DateField(verbose_name='结业日期',blank=True,null=True)
    def __str__(self):
        return '%s-第%s学期'%(self.course,self.semester)
    class Meta:
        unique_together=('course','semester')
        verbose_name_plural='班级表'
    #自定义方法，反向查找每个班级学员的数量，在后台admin里 list_display加上这个"get_student_num"就可以看到
    def get_student_num(self):
        return "%s" % self.customer_set.select_related().count()

    get_student_num.short_description = u'学员数量'

# 9上课记录表
class CourseRecord(models.Model):
    '''上课记录'''
    from_class=models.ForeignKey('ClassList',blank=True,null=True,verbose_name='班级(课程)',on_delete=None)
    day_num=models.PositiveSmallIntegerField(verbose_name='第几节(天)', help_text="此处填写第几节课或第几天课程...,必须为数字")
    teacher=models.ForeignKey('UserProfile',blank=True,null=True,on_delete=None,verbose_name='老师')
    has_homework=models.CharField(max_length=128,blank=True,null=True,verbose_name='作业')
    homework_content=models.TextField(verbose_name='本节课程作业')
    date=models.DateField(auto_now_add=True,verbose_name='上课日期')
    def __str__(self):
        return '%s-%s'%(self.from_class,self.day_num)
    class Meta:
        unique_together=('from_class','day_num')
        verbose_name_plural='上课记录'

# 10学习记录表
class StudyRecord(models.Model):
    '''学习记录'''

    student=models.ForeignKey('Customer',blank=True,null=True,on_delete=None,verbose_name='学员')
    course_record=models.ForeignKey('CourseRecord',blank=True,null=True,on_delete=None,verbose_name='课程记录')
    attendance_choices=((0,'已签到'),
                        (1,'迟到'),
                        (2,'缺勤'),
                        (3,'早退'),)
    attendance=models.SmallIntegerField(choices=attendance_choices,default=0,verbose_name='签到情况')
    score_choices=((100,'A+'),
                   (90,'A'),
                   (85,'B+'),
                   (80,'B'),
                   (75,'B-'),
                   (70,'C+'),
                   (60,'C'),
                   (40,'C-'),
                   (-50,'D'),
                   (--100,'COPY'),
                   (-0,'N/A'),)
    score=models.SmallIntegerField(choices=score_choices,default=0,verbose_name='本节成绩')
    date=models.DateField(auto_now_add=True,verbose_name='日期')
    note=models.TextField(verbose_name='备注',blank=True,null=True)
    def __str__(self):
        return '纪录:%s,学员:%s,成绩:%s'%(self.course_record,self.student,self.score)
    class Meta:
        unique_together=('student','course_record')
        verbose_name_plural='学习记录表'


# 11报名表
class Enrollment(models.Model):
    '''报名表'''
    customer=models.ForeignKey('Customer',blank=True,null=True,on_delete=None,verbose_name='客户')
    school = models.ForeignKey('Branch', verbose_name='校区',on_delete=models.CASCADE,null=True,blank=True)
    enrolled_class=models.ForeignKey('ClassList',blank=True,null=True,verbose_name='所报班级' ,on_delete=None)
    consultant=models.ForeignKey('UserProfile',blank=True,null=True,verbose_name='课程顾问',on_delete=None)
    your_expectation = models.TextField("学完想达到的具体期望", max_length=1024, blank=True, null=True)
    contract_agreed=models.BooleanField(default=False,verbose_name='是否同意协议',help_text='我已认真阅读完培训协议并同意全部协议内容')
    contract_approved=models.BooleanField(default=False,verbose_name='审核通过', help_text=u"在审阅完学员的资料无误后勾选此项,合同即生效")
    enrolled_date=models.DateTimeField('报名日期',auto_now_add=True, auto_created=True,)
    memo = models.TextField('备注', blank=True, null=True)
    def __str__(self):
        return '%s-%s'%(self.customer,self.enrolled_class)
    class Meta:
        unique_together=('customer','enrolled_class')
        verbose_name_plural='报名表'


# 12付款记录表
class Payment(models.Model):
    '''缴费记录'''
    enrollment = models.ForeignKey("Enrollment",on_delete=models.CASCADE,null=True,blank=True)
    pay_type_choices = (('deposit', u"订金/报名费"),
                        ('tution', u"学费"),
                        ('refund', u"退款"),)
    pay_type = models.CharField("费用类型", choices=pay_type_choices, max_length=64, default="tution",null=True,blank=True)
    customer=models.ForeignKey("Customer",blank=True,null=True,on_delete=None,verbose_name='客户')
    course=models.ForeignKey('Course',blank=True,null=True,verbose_name='所报课程',on_delete=models.CASCADE)
    amount=models.PositiveSmallIntegerField(verbose_name='金额',default=0)
    date=models.DateTimeField(auto_now_add=True,verbose_name='交款日期')

    note = models.TextField("备注",blank=True, null=True)
    # paid_fee = models.IntegerField("费用数额", default=0,null=True,blank=True)
    # consultant = models.ForeignKey('UserProfile', verbose_name="负责老师",null=True,blank=True, help_text="谁签的单就选谁",on_delete=models.CASCADE)
    def __str__(self):
        return "%s,数额:%s" % (self.customer, self.amount)
    class Meta:
        verbose_name_plural='缴费记录'



# 14合同模板
class ContractTemplate(models.Model):
    '''合同模板'''
    name=models.CharField(max_length=32,verbose_name='合同名称')
    template=models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='合同表'


class UserProfile(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=32,verbose_name='用户名')
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(_('password'), max_length=128,help_text=mark_safe("<a class='btn-link' href='password/'>点击修改or重置密码</a>"))
    is_active = models.BooleanField(default=True,verbose_name='活动用户')
    is_admin = models.BooleanField(default=False,verbose_name='超级用户')
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=True,
        help_text='Designates whether the user can log into this king_admin site.',
    )
    branch = models.ForeignKey("Branch", verbose_name="所属校区", blank=True, null=True,on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role', blank=True,verbose_name='角色')
    memo = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    objects = auth.UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name_plural = 'CRM账户'
        permissions = (
            ('can_get_acc_logout', '可以退出访问'),
            ('can_get_acc_login', '可以访问登录界面'),
            ('can_post_acc_login', '可以登录'),
            ('can_get_index', '可以访问 king_admin 首页'),
            ('can_get_table_objs', '可以访问 king_admin 各个表'),
            ('can_post_table_objs', '可以修改 king_admin 每个表中对象'),
            ('can_get_edit_detail', '可以查看 king_admin 对应表详细信息'),
            ('can_post_edit_detail', '可以修改 king_admin 对应表详细信息'),
            ('can_get_change_pwd', '可以查看 king_admin 修改密码页面'),
            ('can_post_change_pwd', '可以修改 king_admin 密码'),
            ('can_get_obj_field_delete', '可以查看 king_admin 删除页面'),
            ('can_post_obj_field_delete', '可以修改 king_admin 删除页面数据'),
            ('can_get_obj_table_obj_add', '可以查看 king_admin 新增页面'),
            ('can_post_obj_table_obj_add', '可以修改 king_admin 新增页面数据'),
        )


class StuAccount(models.Model):
    '''存储学员账户信息'''
    account = models.OneToOneField("Customer",on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    valid_start = models.DateTimeField("账户有效期开始",blank=True,null=True)
    valid_end = models.DateTimeField("账户有效期截止",blank=True,null=True)

    def __str__(self):
        return self.account.customer.name

class Role(models.Model):
    '''角色信息'''
    name = models.CharField(max_length=32,unique=True,verbose_name='角色')
    menus = models.ManyToManyField('FirstLayerMenu',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色"

class FirstLayerMenu(models.Model):
    '''第一层侧边栏菜单'''
    name = models.CharField('菜单名',max_length=64)
    url_type_choices = ((0,'related_name'),
                        (1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64,unique=True)
    order = models.SmallIntegerField(default=0,verbose_name='菜单排序')
    sub_menus = models.ManyToManyField('SubMenu',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "第一层菜单"

class SubMenu(models.Model):
    '''第二层侧边栏菜单'''

    name = models.CharField('二层菜单名', max_length=64)
    url_type_choices = ((0,'related_name'),
                        (1,'absolute_url'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=64, unique=True)
    order = models.SmallIntegerField(default=0, verbose_name='菜单排序')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "第二层菜单"