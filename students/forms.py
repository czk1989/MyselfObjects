#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/11/19
from crm.models import UserProfile,Enrollment,Payment
from django.forms import ModelForm,Textarea
from django.forms import ValidationError
from django.utils.translation import ugettext as _
class UserProfileForm(ModelForm):
    def clean(self):
        #
        # is_staff = False
        # roles= models.Role.objects.filter(name='学生').first()
        # self.cleaned_data['is_staff'] = is_staff
        # self.cleaned_data['roles'] = roles
        #
        # self.instance.is_staff = is_staff
        # self.instance.roles = roles
        super().clean()
        # print(dir(self))
        # print(self._clean_fields)
    class Meta:
        model=UserProfile
        fields=['name','email','password','memo']


class EnrooMentForm(ModelForm):
    # def __new__(cls,*args,**kwargs):
    #     for field_name,field_obj in cls.base_fields.items():
    #         field_obj.widget.attrs['class']='form-control'
    #
    #     return ModelForm.__new__(cls)

    def clean_contract_agreed(self):
        contract_agreed = self.cleaned_data['contract_agreed']
        if not contract_agreed:
           raise ValidationError(
                _('Field %(field)s is bool,data should be %(val)s 大神不要黑我了'),
                code='invalid',
                params={'field':contract_agreed,'val':True}
            )
        else:
            return contract_agreed


    class Meta:
        model=Enrollment
        fields=['contract_agreed','consultant','your_expectation']
        widgets = {
            'your_expectation': Textarea(attrs={'width': 20, 'height': 5}),
        }

class PaymentForm(ModelForm):
    # def __init__(self,price):
    #     self.price=price
    # def __new__(cls,*args,**kwargs):
    #     for field_name,field_obj in cls.base_fields.items():
    #         field_obj.widget.attrs['class']='form-control'
    #     return ModelForm.__new__(cls)
    class Meta:
        model=Payment
        fields=['amount']

    # def clean_amount(self):
    #     amount = self.cleaned_data['amount']
    #     if amount!=100:
    #        raise ValidationError(
    #             _('Field %(field)s is bool,data should be %(val)s 大神不要黑我了'),
    #             code='invalid',
    #             params={'field':contract_agreed,'val':True}
    #         )
    #     else:
    #         return amount