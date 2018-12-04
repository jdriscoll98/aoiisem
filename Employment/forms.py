from django import forms
from Employment.models import Employee, Manager
from django.forms import ModelForm

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'
