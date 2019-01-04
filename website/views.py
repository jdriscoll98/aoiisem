from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse_lazy, reverse

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
        return redirect('website:login')


class UpdatePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('website:homepage_view')
