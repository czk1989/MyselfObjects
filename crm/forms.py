#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/10/29
from django.forms import ModelForm
from crm import models

class PaymentForm(ModelForm):
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'
        return ModelForm.__new__(cls)
    class Meta:
        model=models.Payment
        fields='__all__'

class EnrooMentForm(ModelForm):
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'

        return ModelForm.__new__(cls)
    class Meta:
        model=models.Enrollment
        fields=['enrolled_class','consultant']


class CustomerForm(ModelForm):
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class']='form-control'
            if field_name in cls.Meta.readonly_list:
                field_obj.widget.attrs['disabled'] = 'disabled'

        return ModelForm.__new__(cls)
    def clean_qq(self):
        if self.instance.qq!=self.cleaned_data['qq']:
            self.add_error('qq','SB想黑我qq...')
        else:
            return self.cleaned_data['qq']
    def clean_source(self):
        if self.instance.source!=self.cleaned_data['source']:
            self.add_error('source','SB想黑我...')
        else:
            return self.cleaned_data['source']
    def clean_consultant(self):
        if self.instance.consultant!=self.cleaned_data['consultant']:
            self.add_error('consultant','SB想黑我...')
        else:
            return self.cleaned_data['consultant']
    class Meta:
        model=models.Customer
        fields="__all__"
        exclude=['tag','content','referral_from','status','consult_course']
        readonly_list=['qq','source','consultant']