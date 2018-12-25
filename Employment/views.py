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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


from Employment.models import Employee, Clock, Manager
from Employment.forms import ClockForm
from Application.models import Applicant
from Scheduling.models import Availability, Shift, ShiftType, Days
from Scheduling.forms import AvailabilityForm
from django.forms import formset_factory
import json

import datetime
from datetime import timedelta
import calendar

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class ManagerHomePage(UserPassesTestMixin, TemplateView):
    template_name = 'Employment/ManagerHomePage.html'

    def test_func(self):
        return Manager.objects.filter(user=self.request.user).exists()

    def get_context_data(self, **kwargs):
        context = super(ManagerHomePage, self).get_context_data(**kwargs)
        scheduled = []
        default = User.objects.get(username='default')
        for shift in  Shift.objects.filter(date=datetime.date.today()):
            if shift.Type.end_time > datetime.datetime.now().time():
                scheduled.append(shift)
        context = {
            'employees': Employee.objects.exclude(user=default),
            'scheduled': scheduled,
            'manager': self.request.user,
            'applicants': Applicant.objects.filter(old=False),
        #    'clocked': get_clocked_in()
        }
        return context

class EmployeeHomePage(UserPassesTestMixin, TemplateView):
    template_name = 'Employment/EmployeeHomePage.html'

    def test_func(self):
        return Employee.objects.filter(user=self.request.user).exists()

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        today = datetime.date.today()
        context = super(EmployeeHomePage, self).get_context_data(**kwargs)
        context = {
            'employee': self.request.user.employee,
            'shifts': Shift.objects.filter(Employee=employee, date=today),
            'date': str(calendar.day_name[today.weekday()]) + ',' + ' ' + today.strftime('%b, %d'),
            'available': Shift.objects.filter(up_for_trade=True).exclude(Employee=employee),
            'posted': Shift.objects.filter(up_for_trade=True, Employee=employee, date__gte=today)
        }
        return context

class ViewSchedule(LoginRequiredMixin, TemplateView):
    template_name = 'Employment/ViewSchedule.html'

    def get_context_data(self, **kwargs):
        Types = ShiftType.objects.all()
        shifts = Shift.objects.all()
        if len(shifts) >= 30:
            full_schedule = True
        else:
            full_schedule = False

        context = {
            'shifts': shifts,
            'ShiftTypes': Types,
            'days': Days.objects.all(),
            'full_schedule': full_schedule
        }
        return context

class EmployeeDetails(UserPassesTestMixin, TemplateView):
    template_name = 'Employment/EmployeeDetails.html'

    def test_func(self):
        return Manager.objects.filter(user=self.request.user).exists()

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(pk=kwargs['pk'])
        today = datetime.date.today()
        end_of_week = today + timedelta(days=7)
        context = {
            'employee': employee,
            'shifts': Shift.objects.filter(Employee=employee, date__gte=today, date__lte=end_of_week)
        }
        return context

class EmployeeUpdate(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'Employment/employee_update_form.html'

    def test_func(self):
        return Employee.objects.filter(user=self.request.user).exists()

    model = Employee
    fields = ('phone_number', 'email', 'Employee_Number', 'min_hours', 'max_hours')
    success_message = 'Employee Information Updated Successfully'
    success_url = reverse_lazy('Employment:EmployeeHomePage')

class SubmitAvailability(UserPassesTestMixin, View):

    def test_func(self):
        return Employee.objects.filter(user=self.request.user).exists()

    availability_FormSet = formset_factory(AvailabilityForm, max_num=3)
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

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            data = form.cleaned_data
            employee = Employee.objects.get(Employee_Number=data['Employee_Number'])
            data = form.cleaned_data
            user = self.request.user
            employee = Employee.objects.get(Employee_Number=data['Employee_Number'])
            if employee.clocked_in:
                employee.clocked_in = False
                messages.success(self.request, '{0} clocked out successfully'.format(employee))
            else:
                employee.clocked_in = True
                messages.success(self.request, '{0} clocked in successfully'.format(employee))
            employee.save()
            Clock.objects.create(
                employee=employee,
                time = datetime.datetime.now().time(),
                day = datetime.date.today()
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        print('invalid')
        return super(ClockView, self).form_invalid(form)
