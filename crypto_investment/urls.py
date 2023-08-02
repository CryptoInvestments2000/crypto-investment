"""crypto_investment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import(   
    home_view,
)

from members.views import(
    profile_view,
    signup_view,
    login_view,
    logout_view,
    wallet_view,
    withdraw_view,    
    membership_view,
    backoffice_view,
    upgrade_membership_view,   
    approve_withdraw_requests_view,
    team_view,
    withdraw_history
)

urlpatterns = [   
    path('',home_view),   
    path('signup/',signup_view),
    path('login/',login_view),
    path('logout/',logout_view),
    path('profile/', profile_view),    
    path('wallet/', wallet_view),  
    path('withdraw/', withdraw_view),     
    path('membership/',membership_view),
    path('backoffice/',backoffice_view),
    path('upgrade_membership/',upgrade_membership_view),    
    path('approve_withdraw_requests/',approve_withdraw_requests_view),
    path('team/',team_view),
    path('withdraw_history/',withdraw_history),
    path('admin/', admin.site.urls),
]
