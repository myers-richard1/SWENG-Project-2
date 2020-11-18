from django.contrib import admin

# Register your models here.
from .models import Account, ATMachine
    
admin.site.register(Account)
admin.site.register(ATMachine)