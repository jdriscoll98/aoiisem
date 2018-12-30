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

from House.models import House
from Scheduling.models import Shift, SchedulePeriod
from Scheduling.forms import ShiftForm, PostShiftForm
from Employment.models import Employee

from Scheduling.utils import create_schedule
import json

import datetime
from datetime import timedelta

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class UpdateShift(UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'Scheduling/shift_update_form.html'

    def get_success_url(self):
        return reverse_lazy('Employment:EmployeeHomePage')

    def form_valid(self, form):
        employee = Employee.objects.get(user=self.request.user)
        shift = self.object
        if shift.up_for_trade:
            shift.up_for_trade = False
        else:
            shift.up_for_trade = True
        shift.Employee = employee
        shift.save()
        return super(UpdateShift, self).form_valid(form)

class PostShift(FormView):
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
        shift.up_for_trade = True
        shift.save()
        return super(PostShift, self).form_valid(form)

class CreateSchedulePage(TemplateView):
    template_name = 'Scheduling/CreateSchedulePage.html'

class PickUpVacantPage(TemplateView):
    template_name = 'Scheduling/PickUpVacantShift.html'

    def get_context_data(self, *args, **kwargs):
        shift = Shift.objects.get(pk=kwargs['pk'])
        context = {
            'shift': shift,
            'day': shift.date.strftime('%A')
        }
        return context

class PickUpVacant(RedirectView):
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
        scheduleperiod = SchedulePeriod.objects.get(House=House.objects.get(name='AOpi'))
        end_date = scheduleperiod.end_date
        while shift_date < end_date:
            shift = Shift.objects.create(
                Type = shift.Type,
                Employee = employee,
                date = shift_date
            )
            shift_date += timedelta(days = 7)
        return self.get(self, *args, **kwargs)

def CreateSchedule(request):
    if Manager.objects.get(user=user).exists():
         create_schedule(request)
    else:
        return redriect('website:homepage_view')
