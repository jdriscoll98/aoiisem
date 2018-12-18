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
from Scheduling.forms import ShiftForm
from Employment.models import Employee
import json


#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class PickUpShift(UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'Scheduling/shift_update_form.html'

    def get_success_url(self):
        return reverse_lazy('Employment:EmployeeHomePage')

    def form_valid(self, form):
        employee = Employee.objects.get(user=self.request.user)
        self.object.up_for_trade = False
        self.object.Employee = employee
        self.object.save()
        return super(PickUpShift, self).form_valid(form)
