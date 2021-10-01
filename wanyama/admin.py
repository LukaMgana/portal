from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group


admin.site.register([
    Category, Livestock, Tag, 
    ExpenseIncome, Livestock_Health, Report,
    ])
admin.site.unregister(Group)