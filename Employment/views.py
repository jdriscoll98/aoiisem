from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import http
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import TemplateView, View, RedirectView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from core.mixins import ManagerRequired, EmployeeRequired

from django.utils.timezone import now
import pytz
from django.contrib.auth.base_user import BaseUserManager

from Employment.models import Employee, Clock, Manager
from Employment.forms import ClockForm, EmployeeForm
from Application.models import Applicant
from Scheduling.models import Availability, Shift, ShiftType, Days
from Scheduling.forms import AvailabilityForm
from django.forms import formset_factory
import json

from Employment.utils import export_timesheet_data
import datetime
from datetime import timedelta, date
import calendar
import csv

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class ManagerHomePage(ManagerRequired, TemplateView):
    template_name = 'Employment/ManagerHomePage.html'

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
        }
        return context

class EmployeeHomePage(EmployeeRequired, TemplateView):
    template_name = 'Employment/EmployeeHomePage.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        employee = Employee.objects.get(user=self.request.user)
        default = User.objects.get(username='default')
        default_employee = Employee.objects.get(user=default)
        today = datetime.date.today()
        context = super(EmployeeHomePage, self).get_context_data(**kwargs)
        context = {
            'employee': employee,
            'shifts': Shift.objects.filter(Employee=employee, date=today),
            'date': str(calendar.day_name[today.weekday()]) + ',' + ' ' + today.strftime('%b, %d'),
            'available': Shift.objects.filter(is_posted=True).exclude(Employee=employee),
            'vacant': Shift.objects.filter(Employee=default_employee),
            'posted': Shift.objects.filter(is_posted=True, Employee=employee, date__gte=today),
            'trade': Shift.objects.filter(up_for_trade=True)
        }
        return context

class DeleteEmployee(ManagerRequired, DeleteView):
    template_name = 'Employment/DeleteEmployee.html'
    model = Employee
    success_url = reverse_lazy('Employment:ManagerHomePage')

class CreateEmployee(ManagerRequired, FormView):
    template_name = 'Employment/CreateEmployee.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('Employment:ManagerHomePage')

    def form_valid(self, form):
        data = form.cleaned_data
        password = BaseUserManager.make_random_password(self)
        phone_number = str(data['phone_number'])
        code = int(phone_number[-4:])
        user = User.objects.create_user(
            username=(str(data['first_name']) + '_' + str(data['last_name'])),
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password = password
        )
        employee = Employee.objects.create(
            user=user,
            phone_number=phone_number,
            email = user.email,
            Employee_Number = code,
        )
        return super(CreateEmployee, self).form_valid(form)


class ViewSchedule(LoginRequiredMixin, TemplateView):
    template_name = 'Employment/ViewSchedule.html'

    def get_context_data(self, **kwargs):
        Types = ShiftType.objects.all()
        shifts = Shift.objects.all().order_by('pk')
        default = User.objects.get(username='default')
        if len(shifts) >= 30:
            full_schedule = True
        else:
            full_schedule = False

        context = {
            'shifts': shifts,
            'ShiftTypes': Types,
            'days': Days.objects.all(),
            'full_schedule': full_schedule,
            'default': default,
            'self': User.objects.get(username=self.request.user.username)
        }
        return context

class EmployeeDetails(ManagerRequired, TemplateView):
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

class EmployeeUpdate(EmployeeRequired, SuccessMessageMixin, UpdateView):
    template_name = 'Employment/employee_update_form.html'
    model = Employee
    fields = ('phone_number', 'email', 'Employee_Number', 'min_hours', 'max_hours')
    success_message = 'Employee Information Updated Successfully'
    success_url = reverse_lazy('Employment:EmployeeHomePage')

class SubmitAvailability(EmployeeRequired, View):

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
            employee = Employee.objects.get(user=request.user)
            Availability.objects.filter(employee=employee).delete()
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
            user = self.request.user
            if employee.clocked_in:
                employee.clocked_in = False
                inout = 'out'
                messages.success(self.request, '{0} clocked out successfully'.format(employee))
            else:
                employee.clocked_in = True
                inout = 'in'
                messages.success(self.request, '{0} clocked in successfully'.format(employee))
            employee.save()
            Clock.objects.create(
                employee=employee,
                time = datetime.datetime.now(pytz.timezone('US/Eastern')),
                in_out = str(inout)
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        print('invalid')
        return super(ClockView, self).form_invalid(form)

def DownloadTimeSheet(request):
    if Manager.objects.filter(user=request.user).exists():
        return export_timesheet_data()
    else:
        return redirect('website:homepage_view')
