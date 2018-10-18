from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .utils import get_employees, get_shifts
import json

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
@login_required
def homepage_view(request):
    employee = get_employees(request.user)
    context = {
        "employee": employee,
        "shifts" : employee.get_scheduled_shifts(),
        "hours": employee.get_num_of_hours(),
        "pay":  employee.get_num_of_hours() * 8
    }
    print(str(employee.get_scheduled_shifts()))
    return render(request, 'website/homepage.html', context)

def request_time_off_page_view(request):
    context = {
    }
    return render(request, 'website/request_time_off.html', context)

def request_time_off_form_view(request):
    context = {
    }
    return render(request, 'website/request_time_off_form.html', context)

def shifts_available_page_view(request):
    context = {
    }
    return render(request, 'website/shifts_available.html', context)
