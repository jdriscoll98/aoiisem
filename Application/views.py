from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.base_user import BaseUserManager
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, UpdateView,DeleteView
from django.urls import reverse_lazy

from Application.models import Applicant
from Application.forms import ApplicantForm
from Employment.models import Employee
from django.core.mail import send_mail

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
        messages.success(self.request, 'Application Created Successfully')
        return super().form_valid(form)

class UpdateApplication(SuccessMessageMixin, UpdateView):
    template_name = 'Application/UpdateApplicationPage.html'
    model = Applicant
    fields = '__all__'
    success_message = 'Application Updated Successfully'
    def get_success_url(self):
        return reverse_lazy('Application:ApplicationHomePage')

class ApplicantDetails(TemplateView):
    template_name = 'Application/ApplicantDetails.html'
    def get_context_data(self, **kwargs):
        context = {
        'applicant': Applicant.objects.get(pk = kwargs['pk'])
        }
        return context

class AcceptApplicant(SuccessMessageMixin, UpdateView):
    template_name='Application/AcceptApplicant.html'
    model = Applicant
    fields = '__all__'
    success_message = 'Application Accepted Successfully'
    success_url = reverse_lazy('Employment:ManagerHomePage')

    def get_initial(self):
        initial = super(AcceptApplicant, self).get_initial()
        initial['old'] = True
        return initial

    def form_valid(self, form):
        data = form.cleaned_data
        user = data['user']
        phone_number = str(data['phone_number'])
        code = int(phone_number[-4:])
        employee = Employee.objects.create(
            user=user,
            phone_number=phone_number,
            email = user.email,
            pay_rate = int(8),
            Employee_Number = code,
        )
        send_mail(
            'Congratulations!',
            ('You have been accetepted as a new employee! Employee number = {0}'.format(code)),
            'AOii@do-not-reply.com',
            ['{0}'.format(user.email)],
            fail_silently=False,
        )
        return super().form_valid(form)

class DeleteApplicant(DeleteView):
    template_name='Application/DeleteApplicant.html'
    model = Applicant
    fields = '__all__'
    success_url = reverse_lazy('Employment:ManagerHomePage')
