from django import forms
from Application.models import Applicant
from django.forms import ModelForm

class ApplicantForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    class Meta:
        model = Applicant
        exclude = ['user', 'date_submitted']
        fields = ['first_name', 'last_name', 'email', 'Grade', 'statement_of_interest']

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['user'].required = False
            self.fields['user'].widget.attrs['disabled'] = True
            self.fields['date_submitted'].disabled = True
