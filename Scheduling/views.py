from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import http
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.detail import DetailView

from core.mixins import ManagerRequired, EmployeeRequired

from House.models import House
from Scheduling.models import Shift, SchedulePeriod
from Scheduling.forms import ShiftForm, PostShiftForm, SchedulePeriodForm
from Employment.models import Employee

from Scheduling.utils import create_schedule
import json

import datetime
from datetime import timedelta

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class UpdateShift(EmployeeRequired, UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'Scheduling/shift_update_form.html'

    def get_success_url(self):
        return reverse_lazy('Employment:EmployeeHomePage')

    def form_valid(self, form):
        employee = Employee.objects.get(user=self.request.user)
        shift = self.object
        if shift.is_posted:
            shift.is_posted = False
        else:
            shift.is_posted = True
        shift.Employee = employee
        shift.save()
        return super(UpdateShift, self).form_valid(form)

class PostShift(EmployeeRequired, FormView):
    model = Shift
    form_class = PostShiftForm
    template_name = 'Scheduling/shift_update_form.html'

    def get_initial(self):
        initial = super(PostShift, self).get_initial()
        initial['Employee'] = Employee.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_success_url(self):
        return reverse_lazy('Employment:EmployeeHomePage')

    def form_valid(self, form):
        data = form.cleaned_data
        shift = Shift.objects.get(Employee=data['Employee'], date=data['date'], Type=data['Type'])
        shift.is_posted = True
        shift.save()
        return super(PostShift, self).form_valid(form)

class CreateSchedulePage(ManagerRequired, TemplateView):
    template_name = 'Scheduling/CreateSchedulePage.html'

class PickUpVacantPage(EmployeeRequired ,TemplateView):
    template_name = 'Scheduling/PickUpVacantShift.html'

    def get_context_data(self, *args, **kwargs):
        shift = Shift.objects.get(pk=kwargs['pk'])
        context = {
            'shift': shift,
            'day': shift.date.strftime('%A')
        }
        return context

class PickUpVacant(EmployeeRequired, RedirectView):
    permenant = True
    url = reverse_lazy('Employment:EmployeeHomePage')

    def post(self, *args, **kwargs):
        employee = Employee.objects.get(user=self.request.user)
        try:
            shift = Shift.objects.get(pk=kwargs['pk'])
            shift.Employee = employee
            shift.save()
        except Shift.DoesNotExist:
            return http.HttpResponsePermanentRedirect(self.url)
        date = shift.date
        shift_date = date + timedelta(days = 7)
        scheduleperiod = SchedulePeriod.objects.get(House=House.objects.get(pk=1))
        end_date = scheduleperiod.end_date
        while shift_date < end_date:
            shift = Shift.objects.create(
                Type = shift.Type,
                Employee = employee,
                date = shift_date
            )
            shift_date += timedelta(days = 7)
        return self.get(self, *args, **kwargs)

class TradeShiftPage(EmployeeRequired, DetailView):
    model = Shift
    template_name = 'Scheduling/shift.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['self'] = Employee.objects.get(user=self.request.user)
        return context

class TradeShift(EmployeeRequired, RedirectView):
    permenant = True
    url = reverse_lazy('Employment:EmployeeHomePage')

    def post(self, request, *args, **kwargs):
        shift = Shift.objects.get(pk=kwargs['pk'])
        if shift.up_for_trade == True:
            shift.up_for_trade = False
        else:
            shift.up_for_trade = True
        shift.save()
        return self.get(self, *args, **kwargs)

class PickUpPermenantShift(EmployeeRequired, RedirectView):
    permenant = True
    url = reverse_lazy('Employment:EmployeeHomePage')

    def post(self, request, *args, **kwargs):
        shift = Shift.objects.get(pk=kwargs['pk'])
        employee = Employee.objects.get(user=self.request.user)
        Shift.objects.filter(Employee=shift.Employee, Type=shift.Type).update(
        Employee=employee,
        up_for_trade=False
        )
        return self.get(self, *args, **kwargs)

class UpdateSchedulePeriod(ManagerRequired, UpdateView):
    model = SchedulePeriod
    form_class = SchedulePeriodForm
    template_name = 'Scheduling/UpdateSchedulePeriod.html'


def CreateSchedule(request):
    if Manager.objects.get(user=user).exists():
         create_schedule(request)
    else:
        return redriect('website:homepage_view')
