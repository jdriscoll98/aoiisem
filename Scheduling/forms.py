from django import forms
from Scheduling.models import ShiftType, Shift, Availability
from django.forms import CheckboxSelectMultiple
from django.forms import ModelForm

class ShiftTypeForm(ModelForm):
    class Meta:
        model = ShiftType
        fields = '__all__'

class ShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'

class AvailabilityForm(ModelForm):
    class Meta:
        model = Availability
        fields = '__all__'
        widgets = {
            'days' : CheckboxSelectMultiple
        }
