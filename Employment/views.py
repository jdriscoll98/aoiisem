from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy, reverse

from Employment.models import Employee
from Application.models import Applicant
from Scheduling.models import Availability, Shift
from Scheduling.forms import AvailabilityForm
from django.forms import formset_factory
import json

import datetime
from datetime import timedelta
import calendar

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class ManagerHomePage(TemplateView):
    template_name = 'Employment/ManagerHomePage.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerHomePage, self).get_context_data(**kwargs)
        context = {
            'employees': Employee.objects.all,
            'scheduled': Shift.objects.filter(date=datetime.date.today()),
            'manager': self.request.user,
            'applicants': Applicant.objects.all,
        #    'clocked': get_clocked_in()
        }
        return context

class EmployeeHomePage(TemplateView):
    template_name = 'Employment/EmployeeHomePage.html'

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        today = datetime.date.today()
        context = super(EmployeeHomePage, self).get_context_data(**kwargs)
        context = {
            'employee': self.request.user.employee,
            'shifts': Shift.objects.filter(Employee=employee, date=today),
            'date': str(calendar.day_name[today.weekday()]) + ',' + ' ' + today.strftime('%b, %d'),
            'available': Shift.objects.filter(up_for_trade=True).exclude(Employee=employee),
            'posted': Shift.objects.filter(up_for_trade=True, Employee=employee)
        }
        return context

class EmployeeUpdate(UpdateView):
    template_name = 'Employment/employee_update_form.html'
    model = Employee
    fields = ('phone_number', 'email')
    success_url = reverse_lazy('Employment:EmployeeHomePage')

class SubmitAvailability(View):
    Availability_FormSet = formset_factory(AvailabilityForm, extra=3)
    template_name = 'Employment/SubmitAvailability.html'
    success_url = 'Employment:EmployeeHomePage'

    def get(self,request,*args,**kwargs):
        context={
            'availability_form':self.Availability_FormSet(),
            }
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        availability_FormSet=self.Availability_FormSet(self.request.POST)

        if availability_FormSet.is_valid():
            for availability in availability_FormSet:
              availability.save()
            return HttpResponseRedirect(reverse_lazy('Employment:EmployeeHomePage'))
        else:
            context={
                  'availability_form':self.Availability_FormSet(),
                  }
        return render(request,self.template_name,context)
