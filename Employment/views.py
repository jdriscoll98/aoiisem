from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy, reverse

from Employment.models import Employee, Clock

from Employment.forms import ClockForm
from Application.models import Applicant
from Scheduling.models import Availability, Shift, ShiftType
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
            'applicants': Applicant.objects.filter(old=False),
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

class EmployeeDetails(TemplateView):
    template_name = 'Employment/EmployeeDetails.html'

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(pk=kwargs['pk'])
        today = datetime.date.today()
        end_of_week = today + timedelta(days=7)
        context = {
            'employee': employee,
            'shifts': Shift.objects.filter(Employee=employee, date__gte=today, date__lte=end_of_week)
        }
        return context

class EmployeeUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'Employment/employee_update_form.html'
    model = Employee
    fields = ('phone_number', 'email', 'Employee_Number')
    success_message = 'Employee Information Updated Successfully'
    success_url = reverse_lazy('Employment:EmployeeHomePage')

class SubmitAvailability(View):
    availability_FormSet = formset_factory(AvailabilityForm, max_num=len(ShiftType.objects.all()))
    template_name = 'Employment/SubmitAvailability.html'
    success_url = reverse_lazy('Employment:EmployeeHomePage')

    def get(self,request,*args,**kwargs):
        employee=Employee.objects.get(user=self.request.user)
        context={
            'availability_form': self.availability_FormSet(initial=[
            {
                'ShiftType': Type,
                'employee': employee
                }
                for Type in ShiftType.objects.all()])
            }
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        availability_FormSet=self.availability_FormSet(self.request.POST)
        if availability_FormSet.is_valid():
            for availability in availability_FormSet:
                availability.save()
            messages.success(self.request, 'Availability Submitted Successfully')
            return HttpResponseRedirect(reverse_lazy('Employment:EmployeeHomePage'))
        else:
            context={
                  'availability_form':self.Availability_FormSet(),
                  }
        return render(request,self.template_name,context)

class ClockView(FormView):
    template_name = 'Employment/Clock.html'
    form_class = ClockForm
    success_url = reverse_lazy('Employment:Clock')

    def form_valid(self, form):
        data = form.cleaned_data
        user = self.request.user
        employee = Employee.objects.get(Employee_Number=data['Employee_Number'])
        if employee.clocked_in:
            employee.clocked_in = False
            messages.success(self.request, '{0} clocked in successfully'.format(employee))
        else:
            messages.success(self.request, '{0} clocked out successfully'.format(employee))
            employee.clocked_in = True
        employee.save()
        Clock.objects.create(
            employee=employee,
            time = datetime.datetime.now().time(),
            day = datetime.date.today()
        )
        return super(ClockView, self).form_valid(form)

    def form_invalid(self,form):
        print('invalid')
        return super(ClockView, self).form_invalid(form)
