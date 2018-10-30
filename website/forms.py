from django import forms
from .models import Employee

class RequestTimeOffForm(forms.Form):
    DAYS= (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    )
    TYPES=(
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner')
    )
    day = forms.ChoiceField(choices=DAYS)
    type = forms.ChoiceField(choices=TYPES)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())
