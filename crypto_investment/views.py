
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

import os
from pathlib import Path
from django.conf import settings
# from django.conf import 
def home_view(request):   
    print(settings.BASE_DIR)
    return redirect("/login/")