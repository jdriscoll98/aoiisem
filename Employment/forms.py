from django import forms
from Employment.models import Employee, Manager, User
from django.forms import ModelForm

class EmployeeForm(ModelForm):
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    class Meta:
        model = Employee
        exclude = ['user', 'pay_rate', 'Employee_Number', 'clocked_in', 'min_hours', 'max_hours', 'num_hours']
        fields_order = ['first_name', 'last_name', 'phone_number', 'email']

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

class ClockForm(forms.Form):
    Employee_Number = forms.CharField(max_length=4, min_length=4)

    def clean(self):
        cleaned_data = super(ClockForm, self).clean()
        Employee_Number = cleaned_data['Employee_Number']
        try:
            employee = Employee.objects.get(Employee_Number=Employee_Number)
        except Employee.DoesNotExist:
            raise forms.ValidationError('No employee with that number')
        return cleaned_data
