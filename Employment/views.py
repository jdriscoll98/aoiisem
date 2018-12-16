from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from Employment.models import Employee
from Scheduling.models import Availability
from Scheduling.forms import AvailabilityForm
import json

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class ManagerHomePage(TemplateView):
    template_name = 'Employment/ManagerHomePage.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerHomePage, self).get_context_data(**kwargs)
        context = {
            'employees': Employee.objects.all,
            'manager': self.request.user
        }
        return context

class EmployeeHomePage(TemplateView):
    template_name = 'Employment/EmployeeHomePage.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeHomePage, self).get_context_data(**kwargs)
        context = {
            'employee': self.request.user
        }
        return context

class SubmitAvailability(FormView):
    template_name = 'Employment/SubmitAvailability.html'
    form_class = AvailabilityForm
    success_url = reverse_lazy('Employment:EmployeeHomePage')

    def form_valid(self, form):
        data = form.cleaned_data
        days = data['days']
        availability = Availability.objects.create(
            ShiftType = data['ShiftType'],
            employee = self.request.user.employee
        )
        availability.days.add(*days)
        return super(SubmitAvailability, self).form_valid(form)
