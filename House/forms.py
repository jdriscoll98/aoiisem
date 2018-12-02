from django import forms
from .models import House
from django.forms import ModelForm


class HouseForm(ModelForm):
    class Meta:
        model = House
        fields = '__all__'
        widgets = {
            'Primary_color': TextInput(attrs={'type': 'color'}),
            'secondary_color': TextInput(attrs={'type': 'color'})
        }
