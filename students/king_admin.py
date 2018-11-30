#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/11/11
from king_admin.king_admin_base import BaseAdmin,site
from students import models

class StuAccountAdmin(BaseAdmin):
    list_display = ('id','account','profile')
site.register(models.Account,StuAccountAdmin)