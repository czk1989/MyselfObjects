#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/10/25
from crm import auth
from django.forms import ModelForm,Textarea
from django.forms import ValidationError
from django.utils.translation import ugettext as _
from crm import models
#change页面的动态生成数据库类进行编辑,并且进行页面渲染field_obj.help_text,
def create_modelform(request,admin_class):
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            if hasattr(field_obj,'help_text'):
                if getattr(admin_class,'read_only'):
                    pass
                else:
                    field_obj.help_text=''
            if str(type(field_obj))!="<class 'django.forms.fields.BooleanField'>":
                field_obj.widget.attrs['class']='form-control input-sm'
            if getattr(admin_class,'read_only'):
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)


    def default_clean(self):
# read_only参数用来判断页面数据的操作是修改还是增加，如果是新增，就不用判断判断是否有访客修改有display属性的数据
        if getattr(admin_class, 'read_only'):
            for field in admin_class.readonly_fields:
                field_val=getattr(self.instance,field)
                field_val_from_frontend=self.cleaned_data.get(field)
                if field_val!=field_val_from_frontend:
                    raise ValidationError(
                        _('Field %(field)s is readonly,data should be %(val)s 大神不要黑我了'),
                        code='invalid',
                        params={'field':field,'val':field_val}
                    )
    class Meta:
        model=admin_class.models
        fields="__all__"
    attrs={'Meta':Meta}
    _model_form_class=type("DynamicModelForm",(ModelForm,),attrs)
    setattr(_model_form_class,'__new__',__new__)
    setattr(_model_form_class,'clean',default_clean)
    return _model_form_class

def show_modelform(request,admin_class):

    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            if hasattr(field_obj, 'help_text'):
                if getattr(admin_class, 'read_only'):
                    pass
                else:
                    field_obj.help_text = ''
            if str(type(field_obj)) != "<class 'django.forms.fields.BooleanField'>":
                field_obj.widget.attrs['class'] = 'form-control input-sm'
            field_obj.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)
    class Meta:
        model = admin_class.models
        fields = "__all__"

    attrs = {'Meta': Meta}
    _model_form_class = type("DynamicModelForm", (ModelForm,), attrs)
    setattr(_model_form_class, '__new__', __new__)
    return _model_form_class


class EnrooMentForm(ModelForm):
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'

        return ModelForm.__new__(cls)
    class Meta:
        model=models.Enrollment
        fields=['school','enrolled_class','consultant']



class UserProfileForm(ModelForm):
    class Meta:
        model=models.UserProfile
        fields=['name','email','password','memo']
    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user





def creat_account_form(role):

    def default_clean(self):
        self.cleaned_data['is_staff']=False
        self.cleaned_data['roles']=models.Role.objects.filter(name=role).first()

    class Meta:
        model=models.UserProfile
        fields=['name','email','password','memo']

    attrs={'Meta':Meta}
    account=type("CreateModelForm",(ModelForm,),attrs)
    setattr(account,'clean',default_clean)
    return account