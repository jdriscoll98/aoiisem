from django.contrib import admin
from Application.models import Applicant
from Application.forms import ApplicantForm

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    form = ApplicantForm
    fields = ('first_name','last_name', 'email', 'date_submitted', 'statement_of_interest')
