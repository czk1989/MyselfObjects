from django.contrib import admin

# Register your models here.
from students import models
admin.site.register(models.Account)