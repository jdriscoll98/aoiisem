from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .utils import get_employees, get_shifts
from.forms import RequestTimeOffForm
from django.views.generic.edit import FormView, CreateView
from .models import PostShift, Employee, ScheduledShift
import json

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
@login_required
def homepage_view(request):
    employee = get_employees(request.user)
    context = {
        "employee": employee,
        "MondayBreakfast" : employee.get_scheduled_shifts('Monday', 'Breakfast'),
        "TuesdayBreakfast" : employee.get_scheduled_shifts('Tuesday', 'Breakfast'),
        "WednesdayBreakfast" : employee.get_scheduled_shifts('Wednesday', 'Breakfast'),
        "ThursdayBreakfast" : employee.get_scheduled_shifts('Thursday', 'Breakfast'),
        "FridayBreakfast" : employee.get_scheduled_shifts('Friday', 'Breakfast'),
        "MondayLunch" : employee.get_scheduled_shifts('Monday', 'Lunch'),
        "TuesdayLunch" : employee.get_scheduled_shifts('Tuesday', 'Lunch'),
        "WednesdayLunch" : employee.get_scheduled_shifts('Wednesday', 'Lunch'),
        "ThursdayLunch" : employee.get_scheduled_shifts('Thursday', 'Lunch'),
        "FridayLunch" : employee.get_scheduled_shifts('Friday', 'Breakfast'),
        "MondayDinner" : employee.get_scheduled_shifts('Monday', 'Dinner'),
        "TuesdayDinner" : employee.get_scheduled_shifts('Tuesday', 'Dinner'),
        "WednesdayDinner" : employee.get_scheduled_shifts('Wednesday', 'Dinner'),
        "ThursdayDinner" : employee.get_scheduled_shifts('Thursday', 'Dinner'),
        "FridayDinner" : employee.get_scheduled_shifts('Friday', 'Dinner'),
        "Hours" : employee.get_number_of_hours(),
        "money":  employee.get_number_of_hours() * 16
    }
    return render(request, 'website/homepage.html', context)

class PostShiftView(CreateView):
    model = PostShift
    fields = '__all__'
    success_url = '/'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(PostShiftView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        shift = ScheduledShift.objects.get(pk=self.kwargs['pk'])
        employee = Employee.objects.get(user=self.request.user)
        initial = {
            'employee': employee,
            'day': shift.day,
            'type': shift.type
        }
        return initial

def shifts_available_page_view(request):
    context = {
    }
    return render(request, 'website/shifts_available.html', context)
