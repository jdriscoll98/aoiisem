from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.base_user import BaseUserManager
from django.core import serializers

from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy

from Application.models import Applicant
from Application.forms import ApplicantForm

import datetime
import json

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class ApplicationHomePage(TemplateView):
    template_name = 'Application/ApplicationHomePage.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationHomePage, self).get_context_data(**kwargs)
        context = {
            'applicant': Applicant.objects.get(user=self.request.user),
        }
        return context


class NewApplication(FormView):
    template_name = 'Application/NewApplicationPage.html'
    form_class = ApplicantForm
    success_url = reverse_lazy('Application:ApplicantHomePage')

    def form_valid(self, form):
        data = form.cleaned_data
        password = BaseUserManager.make_random_password(self)
        user = User.objects.create_user(
            username = data['first_name'] + '_' + data['last_name'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password = password,
        )
        Applicant.objects.create(
            user= user,
            date_submitted = datetime.date.today(),
            Grade = data['Grade'],
            statement_of_interest = data['statement_of_interest']
        )
        return super().form_valid(form)

class UpdateApplication(UpdateView):
    template_name = 'Application/UpdateApplicationPage.html'
    model = Applicant
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('Application:ApplicantHomePage')
