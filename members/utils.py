import random
from .models import CustomUser, Settings
from datetime import date

def generate_referrel_code():
    referrel_code = random.randint(1_000_000_000,9_000_000_000)
    qs = CustomUser.search_member_by_referrel(referrel_code)
    if qs is None:
        return referrel_code
    else:
        generate_referrel_code()

def isNum(data):
    try:
        float(data)
        return True
    except ValueError:
        return False
def introducer_commission(membership,level):
    commission = 0
    if level == 1:
        if membership == 'Bronze':
            commission = 1        
        elif membership == "Silver":
            commission = 2        
        elif membership == "Gold":
            commission = 3
        elif membership == 'Platinum':
            commission = 4
        elif membership == 'Diamond':
            commission = 5
        else:
            commission=0
        
    if level == 2:
        if membership == 'Bronze':
            commission = 1        
        elif membership == "Silver":
            commission = 2        
        elif membership == "Gold":
            commission = 3
        elif membership == 'Platinum':
            commission = 4
        elif membership == 'Diamond':
            commission = 5
        else:
            commission=0
    if level == 3:        
        if membership == 'Bronze':
            commission = 1        
        elif membership == "Silver":
            commission = 2        
        elif membership == "Gold":
            commission = 3
        elif membership == 'Platinum':
            commission = 4
        elif membership == 'Diamond':
            commission = 5
        else:
            commission=0
    return commission

def get_minimum_withdraw_amount(membership):
    amount = 0
    if membership == 'Bronze':
        amount = 10        
    elif membership == "Silver":
        amount= 20       
    elif membership == "Gold":
        amount = 60
    elif membership == 'Platinum':
        amount = 100
    elif membership == 'Diamond':
        amount = 200
    else:
        amount = 0
    return amount


def calculate_daily_interest(member):
    qs = CustomUser.objects.exclude(username = member).values()        
    username = member.username
    membership = member.membership
    daily_income = member.daily_income
    total_earnings = member.total_earnings
    balance = member.balance    
    last_interest_calculation = member.date_interest_calculated
    date_today = date.today()   
    date_diff = date_today - last_interest_calculation 
    date_diff = date_diff.days
    if date_diff != 0 and membership != 'None':        
        
        #calculate today's income

        todays_income = 0
        if membership == 'Bronze':
            todays_income = 2 
        elif membership == "Silver":
            todays_income= 4
        elif membership == "Gold":
            todays_income = 12
        elif membership == 'Platinum':
            todays_income= 20
        elif membership == 'Diamond':
            todays_income= 40
        else:
            todays_income=0
        
        
        todays_income *= date_diff
        daily_income += todays_income
        total_earnings += todays_income
        balance += todays_income

        #Update CustomUser
        update_member = CustomUser.objects.get(username=username)
        update_member.daily_income = daily_income   
        update_member.total_earnings = total_earnings
        update_member.balance = balance
        update_member.save()
      
    