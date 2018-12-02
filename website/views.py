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
    context = {
    }
    return render(request, 'website/homepage.html', context)
