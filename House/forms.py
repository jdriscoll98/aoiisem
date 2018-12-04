from django import forms
from .models import House
from django.forms.widgets import TextInput
from django.forms import ModelForm


class HouseForm(ModelForm):
    class Meta:
        model = House
        fields = '__all__'
        widgets = {
            'primary_color': TextInput(attrs={'type': 'color'}),
            'secondary_color': TextInput(attrs={'type': 'color'})
        }
