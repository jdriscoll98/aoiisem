from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView

from Scheduling.models import Shift
from Scheduling.forms import ShiftForm, PostShiftForm
from Employment.models import Employee
import json


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
