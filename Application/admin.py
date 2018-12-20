from django.contrib import admin
from Application.models import Applicant
from Application.forms import ApplicantForm

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant
    fields = ('user', 'Grade', 'statement_of_interest')
    list_display = ('user', 'date_submitted', 'Grade')
