from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import json

from Employment.models import Employee, Manager
from Application.models import Applicant

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
@login_required
def homepage_view(request):
    user = request.user
    if Manager.objects.filter(user=user).exists():
        return redirect('Employment:ManagerHomePage')
    elif Employee.objects.filter(user=user).exists():
        return redirect('Employment:EmployeeHomePage')
    elif Applicant.objects.filter(user=user).exists():
        return redirect('Application:ApplicationHomePage')
    else:
        return redirect('website:logout')
