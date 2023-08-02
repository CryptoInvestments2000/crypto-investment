from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WithdrawRequest, UpgradeRequest, Settings

class SettingsAdmin(admin.ModelAdmin):
    list_display=(
        'company_usdt_address',
    )

    fieldsets = (
        (None,{
            'fields':('company_usdt_address',)
        }),
    )

    add_fieldsets = (
        (None,{
            'fields':('company_usdt_address',)
        }),
    )

admin.site.register(Settings,SettingsAdmin)   

class UpgradeRequestAdmin(admin.ModelAdmin):
    list_display=(
        'trans_id','username','request_date','membership','due_amount','upgraded'
    )

    search_fields = ('trans_id', 'username','status')

    fieldsets = (
        (None, {
            'fields': ('trans_id','username','request_date','membership','due_amount','upgraded')
        }),     )

    
    add_fieldsets = (
        (None, {
            'fields': ('trans_id','username','request_date','membership','due_amount','upgraded')
        }), 
    )

admin.site.register(UpgradeRequest,UpgradeRequestAdmin)   

class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display=(
        'request_date','username','amount','usdt_address','paid','paid_date'
    )

    search_fields = ('username','usdt_address','paid')


    fieldsets = (
        (None, {
            'fields': ('request_date','username','amount','usdt_address','paid','paid_date')
        }), 
    )

    add_fieldsets = (
        (None, {
            'fields': ('request_date','username','amount','usdt_address','paid','paid_date')
        }), 
    )

admin.site.register(WithdrawRequest,WithdrawRequestAdmin)   

class CustomUserAdmin(UserAdmin):    
    list_display = (
        'username','introducer', 'referrel_code','membership','date_upgraded','budget',  
        'balance','total_withdrawals','total_earnings','daily_income',
        'level1_com','level2_com','level3_com','usdt_address','is_active')

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }), 
        ('Additional info', {
            'fields': ('introducer', 'referrel_code','membership',
            'budget','balance','total_withdrawals','total_earnings','daily_income','level1_com',
            'level2_com','level3_com','usdt_address')
        }),       
        ('Permissions', {
            'fields': ('is_active',)   
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined','date_upgraded')
        }),
        
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }), 
         ('Additional info', {
            'fields': ('introducer', 'referrel_code','membership',
            'budget','balance','total_withdrawals','total_earnings','daily_income','level1_com',
            'level2_com','level3_com','usdt_address')
        }),           
        ('Permissions', {
            'fields': ('is_active',)                
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined','date_upgraded')
        }),
       
    )

admin.site.register(CustomUser, CustomUserAdmin)
