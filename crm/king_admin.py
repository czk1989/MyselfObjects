#_*_coding:utf-8_*_

from crm import models
from django import forms

from king_admin.king_admin_base import BaseAdmin,site

# class MultiDBModelAdmin(admin.ModelAdmin):
class CustomerAdmin(BaseAdmin):
    model = models.Customer
    list_display = ['id','name','qq','phone','source','consultant','status','date','enroll']
    # list_editable = ['phone',"source","consultant",'status']
    # fk_fields = ['consultant']
    # choice_fields = ['source','status']
    filter_horizontal=['tag']
    list_filters = ['source','consultant','status']
    readonly_fields = ['qq','referral_from','consultant','status']
    list_search = ['qq','email']
    colored_fields = {
        'status':{'已报名':"rgba(145, 255, 0, 0.78)",
                  '未报名':"#ddd"},
    }

    def enroll(self):
        '''报名'''
        # print("customize field enroll",self)
        link_name = "报名"
        if self.instance.status ==1:
            link_name = "报名新课程"
        return '''<a class="btn-link" href="/crm/enrollment/%s/">%s</a> ''' % (self.instance.id,link_name)
    enroll.display_name = "报名链接"

# 11报名表
class EnrollmentAdmin(BaseAdmin):
    model = models.Enrollment
    list_display = ['id','customer','school','enrolled_class','contract_agreed','contract_approved','enrolled_date']
    list_search = ['school__name','customer__name']
    list_filters=['enrolled_class','enrolled_date']

# 8班级表
class ClasslistAdmin(BaseAdmin):
    model=models.ClassList
    list_display = ['id','branch','course','semester','class_type','start_date']
    list_search= ['branch__name','course__name']
    filter_horizontal = ['teachers']
    # default_actions = ['delete_selected']
    #readonly_table = True
    readonly_fields = ['price','semester']
    list_filters=['course','class_type']

# 12付款记录表
class PaymentAdmin(BaseAdmin):
    model = models.Payment
    list_filters = ('course','date')
    list_display = ('id','enrollment','course','amount','date')
    # fk_fields = ('enrollment','consultant')
    # choice_fields = ('')
    list_search=['amount']


# 9上课记录表
class CourseRecordAdmin(BaseAdmin):
    model = models.CourseRecord
    list_display = ['id','from_class','day_num','date','teacher','has_homework']
    # fk_fields = ['from_class','teacher']
    list_filters = ['from_class','teacher','has_homework','date']
    list_search = ['day_num']
    # def study_records(self):
    #     ele = '''<a class="btn-link" href='/crm/crm_studyrecord/?&course_record=%s' >学员成绩</a>''' \
    #           %(self.instance.id)
    #
    #     return ele
    # study_records.display_name = "学员学习记录"

# 10学习记录表
class StudyRecordAdmin(BaseAdmin):
    model=models.StudyRecord
    list_display = ["id",'course_record','student','attendance','score','date','note']
    list_filters = ['attendance','date']
    choice_fields = ['record','score']
    list_search = ['student__name','score']
    # fk_fields = ['student','course_record']
    # list_editable = ['id','student','record','score','note']



#暂时还没有用这个功能
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email','name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入密码不匹配")
        if len(password1) < 6:
            raise forms.ValidationError("密码长度小于6位")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileAdmin(BaseAdmin):
    add_form = UserCreationForm
    model=models.UserProfile
    list_display = ['id','email','is_staff','is_admin']
    list_search = ['branch__name','roles__name']
    list_filters = ['roles','branch']
    readonly_fields = ['password',]
    change_page_onclick_fields = {
        'password':['password','重置密码']
    }
    filter_horizontal = ('user_permissions','roles')
    # list_editable = ['is_admin','is_superuser']

class FirstLayerMenuAdmin(BaseAdmin):
    model = models.FirstLayerMenu
    list_display = ('id','name','url_type','url_name',)
    choice_fields = ['url_type']

class SubMenuAdmin(BaseAdmin):
    model = models.FirstLayerMenu
    list_display = ('id','name','url_type','url_name')
    choice_fields = ['url_type']

class RoleAdmin(BaseAdmin):
    model=models.Role
    list_display = ['id','name']
    filter_horizontal = ['menus']
    list_search = ['name']
    list_filters = []

# 6课程表
class CourseAdmin(BaseAdmin):
    model=models.Course
    list_display = ['id','name','period']
    list_search = ['name']
    list_filters = ['period']

# 7校区表
class BranchAdmin(BaseAdmin):
    model=models.Course
    list_display = ['id','name','addr']
    list_search = ['name']
    list_filters = []

class ContractTemplateAdmin(BaseAdmin):
    model=models.Course
    list_display = ['id','name']
    list_search = ['name']
    list_filters = []

class TagAdmin(BaseAdmin):
    model=models.Tag
    list_display = ['id','name']
    list_search = ['name']
    list_filters = []

site.register(models.Customer,CustomerAdmin)
site.register(models.ClassList,ClasslistAdmin)
site.register(models.Enrollment,EnrollmentAdmin)
site.register(models.Payment,PaymentAdmin)
site.register(models.CourseRecord,CourseRecordAdmin)
site.register(models.StudyRecord,StudyRecordAdmin)
site.register(models.UserProfile,UserProfileAdmin)
site.register(models.FirstLayerMenu,FirstLayerMenuAdmin)
site.register(models.SubMenu,SubMenuAdmin)
site.register(models.Role,RoleAdmin)
site.register(models.Course,CourseAdmin)
site.register(models.Branch,BranchAdmin)
site.register(models.ContractTemplate,ContractTemplateAdmin)
site.register(models.Tag,TagAdmin)

