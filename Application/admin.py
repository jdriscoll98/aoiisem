from django.contrib import admin
from Application.models import Applicant
from Application.forms import ApplicantForm

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant
    fields = ('user', 'Grade', 'phone_number', 'statement_of_interest', 'date_submitted', 'old')
    list_display = ('user', 'date_submitted', 'Grade')
