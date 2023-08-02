
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignUpForm
from .models import CustomUser, UpdateUserUSDT,UpgradeRequest, Settings, WithdrawRequest
from .utils import generate_referrel_code, isNum, introducer_commission, get_minimum_withdraw_amount,calculate_daily_interest
from datetime import date


def signup_view(request):  
    if request.user.is_anonymous:  
        if request.method == "POST":   
            form = SignUpForm(request.POST)    
            if form.is_valid:  
                referrel_code = request.POST.get('referrel_code')                
                introducer = CustomUser.search_member_by_referrel(referrel_code) 
                user = form.save(commit=False)    
                # user.is_active = False
                user.save()
                return redirect("/login/")   
            else:
                context = {
                    "form":form
                }
                return render(request,"templates/members/signup.html",context) 
                  
                
    else:        
        return redirect("/profile/")
    introducer=''
    if request.method == 'GET':
        introducer = request.GET.get('q', '')
        introducer = CustomUser.search_member_by_referrel(introducer)
        if introducer is None:
             introducer =''           
     
    referrel_code = generate_referrel_code()    
    form = SignUpForm(initial={'introducer': introducer, 'referrel_code': referrel_code})         
    context = {
        "form":form
    }
    return render(request,"templates/members/signup.html",context)

def login_view(request):        
    if request.method == "POST":       
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)            
            return redirect('/profile/')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, "templates/members/login.html", context)

def logout_view(request):
    logout(request)    
    return redirect("/")    

@login_required
def profile_view(request):    
    username = request.user
    if request.method == 'POST':
        usdt_address = request.POST.get('usdt_address')        
        if usdt_address is not None:            
            form = UpdateUserUSDT(data=request.POST, instance=username) 
            if form.is_valid():
                user = form.save()                
                user.save()
             
    dict = CustomUser.get_member_details_by_username(username)  
    member = dict.get(username=username)      
    context= {       
        'member': member,                
        }
    return render(request,'templates/members/profile.html',context)

@login_required
def wallet_view(request):
    username = request.user    
    calculate_daily_interest(username)
    qs = CustomUser.get_member_details_by_username(username)       
    context= {       
        'objects_list': qs,        
        }
    return render(request,'templates/members/wallet.html',context)


@login_required
def withdraw_view(request):
    username = request.user    
    dict = CustomUser.get_member_details_by_username(username)  
    member = dict.get(username=username)
    membership = member.get('membership')    

    # Check for membership
    if membership == 'None':
            message = 'Upgrade your membership to withdraw money!!!' 
            redirect_to = '/membership/'
            context= {       
                'member':member,
                'message':message,
                'redirect_to': redirect_to            
            }      
            return render(request,'templates/members/message.html',context)
    if request.method == 'POST':
        has_error = False        
        budget = member.get('budget')
        balance = member.get('balance')
        usdt_address = request.POST.get('usdt_address')
        withdraw_amount = request.POST.get('withdraw_amount')   
        redirect_to = '/wallet/'
        if isNum(withdraw_amount) == False:
            has_error = True 
            message = 'Enter a valid amount to withdraw!!!'            
            redirect_to = '/withdraw/'  
        else:
            amount =  float(withdraw_amount)             
            if amount > balance:  
                has_error = True
                message = "You don't have enough Wallet Balance !!!"
                redirect_to = '/withdraw/'
            else:
                min_amount = get_minimum_withdraw_amount(membership)
                if amount < min_amount:
                    has_error = True
                    message = "Your minimum withdraw amount is USDT " + str(min_amount)
                    redirect_to = '/withdraw/'
                else:
                    if amount > budget:                
                        has_error = True
                        message = "Your maximum withdraw amount is USDT " + str(budget) + " !!! \nInvite friends to increase your budget. \nYour invitation link is in the 'Profile' page"
                        redirect_to = '/profile/'
                    else:
                        # update customuser
                        member = CustomUser.objects.get(username=username)
                        total_withdrawal = member.total_withdrawals
                        new_budget = budget - int(withdraw_amount)
                        new_balance = balance - int(withdraw_amount)
                        new_total_withdrawal = int(total_withdrawal) + int(withdraw_amount)
                        member.budget = new_budget
                        member.balance = new_balance
                        member.total_withdrawals = new_total_withdrawal
                        member.save()

                        # Add to WithdrawRequests
                        withdraw_amount = int(withdraw_amount)
                        request_date = date.today()
                        WithdrawRequest.objects.create(request_date=request_date,username=username,
                                        amount=withdraw_amount,usdt_address=usdt_address,paid=False)      
                        
        if has_error == False:
            message = 'Your withdraw request sent. Service fee of 10% will be charged.'
        context= {       
            'member':member,
            'message':message,
            'redirect_to': redirect_to            
        }      
        return render(request,'templates/members/message.html',context)
    context= {       
        'member':member,            
        }
    return render(request,'templates/members/withdraw.html',context)

@login_required
def membership_view(request):
    username = request.user    
    dict = CustomUser.get_member_details_by_username(username)  
    member = dict.get(username=username)
    if request.method == 'POST':
        # check for pending upgrades
        member = UpgradeRequest.objects.filter(username=username,upgraded=False)        
        if not member:
            pass
        else:
            message = 'You have pending upgrade requests'
            member = username            
            redirect_to = '/profile/'
            context = {
                'message':message,
                'member' : username,
                'redirect_to': redirect_to  
            }
            return render(request,'templates/members/message.html',context)
        trans_id = request.POST.get('trans_id')  
        membership = request.POST.get('membership')
        membership = membership.strip()      
        if membership == 'Bronze':
            due_amount = 50
        elif membership == "Silver":
           due_amount=100
        elif membership == "Gold":
            due_amount = 300
        elif membership == 'Platinum':
            due_amount=500
        elif membership == 'Diamond':
            due_amount=1000
        else:
            due_amount=0
        
        request_date = date.today() 
        has_error = False
        if trans_id is None or trans_id=='':
            message = "Enter your Binance transaction reference number..." 
            has_error = True
        elif membership == 'None':
            message = "Select a membership..."
            has_error = True
        if has_error == True:
            redirect_to = '/membership/'
            context = {
                'message':message,   
                'member': member,
                'redirect_to' : redirect_to      
            }
            return render(request,'templates/members/message.html',context)
        upgrademembership = UpgradeRequest.objects.create(
            trans_id=trans_id,username=username,
            request_date=request_date,membership=membership,
            due_amount=due_amount
            )
        
        message = "Upgrade Request Sent. Your membership will be upgraded after verification."
        redirect_to = '/profile/'
        context = {
            'message':message,   
            'member': member,
            'redirect_to' : redirect_to
        }
        return render(request,'templates/members/message.html',context)
    
    member = dict.get(username=username)
    company_usdt_address = Settings.objects.values_list('company_usdt_address',flat=True).first()          
    context = {
        'member':member,
        'company_usdt_address':company_usdt_address
    }
    return render(request,'templates/members/membership.html',context)

@login_required
def team_view(request):
    username = request.user
    member = CustomUser.objects.get(username = username)
    level1_members = CustomUser.objects.filter(introducer=member)
    level1_count = 0
    level2_count = 0
    level3_count = 0
    for level1_member in level1_members:
        level1_count += 1   
        level2_members = CustomUser.objects.filter(introducer = level1_member)
        for level2_member in level2_members:
            level2_count += 1
            level3_members = CustomUser.objects.filter(introducer = level2_member)
            for level3_member in level3_members:
                level3_count += 1

    context = {
        'username' : username,
        'level1_count': level1_count,
        'level2_count': level2_count,
        'level3_count': level3_count
    }
    return render(request,'templates/members/team.html',context)

@login_required
def withdraw_history(request):
    username = request.user
    withdraw_history = WithdrawRequest.objects.filter(username = username)
    print(withdraw_history)
    context={      
        "withdraw_history_obj": withdraw_history,
        "username" : username
    }
    return render(request,'templates/members/withdraw_history.html',context)

@user_passes_test(lambda u: u.is_superuser)
def backoffice_view(request):
    #Total budget reserves
    total_budget = 0
    qs = CustomUser.objects.values_list('budget',flat=True)    
    for budget in qs:   
        total_budget = total_budget + budget
    
    # #Calculating my profit
    qs = UpgradeRequest.objects.filter(upgraded=True).values_list('due_amount',flat=True)
    my_profit= 0
    for due_amount in qs:        
        my_profit = my_profit + ( due_amount * 0.2 )

    #Last member interest calculation
    last_interest_calculation = Settings.objects.values_list('last_interest_calculation',flat=True).first()
    date_today = date.today()
    date_diff = date_today - last_interest_calculation
    
    #Calculating my earnings
    context={
        'my_profit' : my_profit,
        'total_budget':total_budget,
        'last_interest_calculation' : last_interest_calculation,
        'date_diff' : date_diff.days
        
    }
    return render(request,'templates/members/backoffice.html',context)

@user_passes_test(lambda u: u.is_superuser)
def upgrade_membership_view(request):
    if "upgrade_membership" in request.POST:
        username = request.POST.get('username')
        membership = request.POST.get('membership')

        #Update CustomUser
        member = CustomUser.objects.get(username=username)
        member.membership = membership
        budget = member.budget
        add_amount = 0
        if membership == 'Bronze':
            plan_value = 50 
        elif membership == "Silver":
            plan_value=100
        elif membership == "Gold":
            plan_value = 300
        elif membership == 'Platinum':
            plan_value=500
        elif membership == 'Diamond':
            plan_value=1000
        else:
            plan_value=0
      
        if plan_value != 0:
            add_amount = plan_value * 0.65
        budget = budget + add_amount
        member.budget = budget
        member.date_upgraded = date.today()       
        member.date_interest_calculated = date.today()
        member.save()

        #Update UpgradeRequest

        upgrade_request = UpgradeRequest.objects.get(username=username, upgraded=False)
        upgrade_request.upgraded = True        
        upgrade_request.save()

        #Increase introducer budget

        introducer_budget_increase = plan_value * 0.15
        introducer_name = member.introducer
        print(introducer_name)
        if introducer_name != '':
            introducer = CustomUser.objects.get(username=introducer_name)        
            introducer_budget = introducer.budget
            introducer.budget = introducer_budget + introducer_budget_increase
            introducer.save()

    qs = UpgradeRequest.objects.filter(upgraded=False)   
    context = {
        'object_list':qs,        
    }
    return render(request,'templates/members/upgrade_membership.html',context)

@user_passes_test(lambda u: u.is_superuser)
def approve_withdraw_requests_view(request):
    if "approve_withdraw_request" in request.POST:
        id = request.POST.get('id')        
        withdraw_request = WithdrawRequest.objects.get(id=id)
        username = withdraw_request.username
        amount = withdraw_request.amount
        withdraw_request.paid = True
        withdraw_request.save()

        #Commission Calculation
        member = CustomUser.objects.get(username=username)
        introducer_level_1 = member.introducer
        if introducer_level_1 != '':
            introducer_level_1_obj = CustomUser.objects.get(username = introducer_level_1)
            introducer_level_1_membership = introducer_level_1_obj.membership
            percentage = introducer_commission(introducer_level_1_membership,1)
            commission = amount * (percentage / 100)
            level1_com = introducer_level_1_obj.level1_com
            balance =  introducer_level_1_obj.balance 
            introducer_level_1_obj.level1_com = level1_com + commission
            introducer_level_1_obj.balance  = balance + commission
            introducer_level_1_obj.save()
           
            introducer_level_2 = introducer_level_1_obj.introducer
            if introducer_level_2 != '':
                introducer_level_2_obj = CustomUser.objects.get(username = introducer_level_2)
                introducer_level_2_membership = introducer_level_2_obj.membership
                percentage = introducer_commission(introducer_level_2_membership,2)
                commission = amount * (percentage / 100)
                level2_com = introducer_level_2_obj.level2_com
                balance =  introducer_level_2_obj.balance 
                introducer_level_2_obj.level2_com = level2_com + commission
                introducer_level_2_obj.balance = balance + commission
                introducer_level_2_obj.save()

                introducer_level_3 = introducer_level_2_obj.introducer
                if introducer_level_3 != '':
                    introducer_level_3_obj = CustomUser.objects.get(username = introducer_level_3)
                    introducer_level_3_membership = introducer_level_3_obj.membership
                    percentage = introducer_commission(introducer_level_3_membership,3)
                    commission = amount * (percentage / 100)
                    level3_com = introducer_level_3_obj.level3_com
                    balance =  introducer_level_3_obj.balance 
                    introducer_level_3_obj.level3_com = level3_com + commission
                    introducer_level_3_obj.balance = balance + commission
                    introducer_level_3_obj.save()


    qs = WithdrawRequest.objects.filter(paid=False)   
    context = {
        'object_list':qs,        
    }
    return render(request,'templates/members/withdraw_requests.html',context)