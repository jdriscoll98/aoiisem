from django import forms
from Employment.models import Employee, Manager, User
from django.forms import ModelForm

class EmployeeForm(ModelForm):
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    class Meta:
        model = Employee
        exclude = ['user']

    def clean(self):
        cleaned_data = super(EmployeeForm, self).clean()
        try:
            employee = Employee.objects.get(email=cleaned_data['email'])
            raise forms.ValidationError('This email is already in use')
        except Employee.DoesNotExist:
            pass
        try:
            employee = User.objects.get(first_name=cleaned_data['first_name'], last_name=cleaned_data['last_name'])
            raise forms.ValidationError('This employee already exists')
        except User.DoesNotExist:
            pass
        try:
            employee = Employee.objects.get(phone_number=cleaned_data['phone_number'])
            raise forms.ValidationError('This phone number is already in use')
        except Employee.DoesNotExist:
            pass
        return cleaned_data

class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'
