from django import forms
from Scheduling.models import ShiftType, Shift, Availability, SchedulePeriod
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

class SchedulePeriodForm(ModelForm):
    class Meta:
        model = SchedulePeriod
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'class':'datepicker'}),
            'end_date': forms.DateInput(attrs={'class':'datepicker'})
        }

    def clean(self):
        cleaned_data = super(SchedulePeriodForm, self).clean()
        start_date, end_date= cleaned_data['start_date'], cleaned_data['end_date']
        if end_date > start_date:
            pass
        else:
            raise forms.ValidationError('The end date must be after the start date')
        return cleaned_data
