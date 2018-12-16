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

    def clean(self):
        cleaned_data = super(HouseForm, self).clean()
        name = cleaned_data['name']
        try:
            already_exist_house = House.objects.get(name=name)
            raise forms.ValidationError("House already exists")
        except House.DoesNotExist:
            pass
        return cleaned_data
