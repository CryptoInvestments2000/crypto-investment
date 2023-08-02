from django.db import models
from django.db.models import Q
from datetime import datetime,date 
from django.contrib.auth.models import AbstractUser
from django import forms

class UpgradeRequest(models.Model):
    trans_id = models.CharField(max_length=100, unique=True,blank=False)
    username = models.CharField(max_length=15, blank=False)
    request_date = models.DateField(default=date.today)
    membership = models.CharField(max_length=15, blank=False)
    due_amount = models.FloatField(default=0)
    upgraded = models.BooleanField(default=False)

    class Meta:
         verbose_name = "Upgrade Request"
         verbose_name_plural = "Upgrade Requests"


class WithdrawRequest(models.Model):       
    request_date= models.DateField()
    username = models.CharField(max_length=200, blank=True)
    amount = models.FloatField(default=0)
    usdt_address = models.CharField(max_length=200,default='None')
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(default=date.today)

    class Meta:
         verbose_name = "Withdraw Request"
         verbose_name_plural = "Withdraw Requests"


class CustomUser(AbstractUser):   
    introducer = models.CharField(max_length=200, blank=True)
    referrel_code = models.CharField(max_length=10, blank=True)
    membership = models.CharField(max_length=10,blank=True,default='None',choices=[
                    ('None', 'None'), 
                    ('Bronze', 'Bronze'),
                    ('Silver', 'Silver'),
                    ('Gold', 'Gold'),
                    ('Platinum', 'Platinum'),
                    ('Diamond', 'Diamond')
                    ])
    budget = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    total_withdrawals = models.FloatField(default=0)
    total_earnings = models.FloatField(default=0)
    daily_income = models.FloatField(default=0)
    level1_com = models.FloatField(default=0)
    level2_com = models.FloatField(default=0)
    level3_com = models.FloatField(default=0)
    usdt_address =models.CharField(max_length=200,blank=True)
    date_upgraded = models.DateField(default=date.today)
    date_interest_calculated = models.DateField(default=date.today)

    
    def search_member_by_referrel(query):         
        if query is None or query=="":
            return None
        lookups = Q(referrel_code=query)
        qs =  CustomUser.objects.all().filter(lookups)
        if qs.exists():
            return qs.first()
        else:
            return None
    
    def get_member_details_by_username(query):         
        if query is None or query=="":
            return CustomUser.none()
        lookups = Q(username=query)
        qs =  CustomUser.objects.filter(lookups).values()
        if qs.exists():
            return qs
        else:
            return None      
    
    class Meta:
         verbose_name = "Member"
         verbose_name_plural = "Members"
    
class UpdateUserUSDT(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['usdt_address']

class Settings(models.Model):    
    company_usdt_address =models.CharField(max_length=200,blank=True)
    class Meta:
         verbose_name = "Settings"
         verbose_name_plural = "Settings"
    
    

    

