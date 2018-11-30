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
        super().clean()

    class Meta:
        model=UserProfile
        fields=['name','email','password','memo']


class EnrooMentForm(ModelForm):

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

    class Meta:
        model=Payment
        fields=['amount']
