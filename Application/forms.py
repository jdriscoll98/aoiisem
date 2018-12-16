from django import forms
from Application.models import Applicant
from django.forms import ModelForm

class ApplicantForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    class Meta:
        model = Applicant
        exclude = ['user']
