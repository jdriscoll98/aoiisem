from django.contrib import admin
from Scheduling.models import Days, ShiftType, Shift, Availability
from Scheduling.forms import AvailabilityForm

admin.site.register(ShiftType)
admin.site.register(Days)
admin.site.register(Shift)

@admin.register(Availability)
class AvailabiltyAdmin(admin.ModelAdmin):
    form = AvailabilityForm
    fieldsets = (
        (None, {
            'fields': ('ShiftType', 'days', 'employee')
            }),
        )
