from django.contrib import admin
from Scheduling.models import Days, ShiftType, Shift, Availability

admin.site.register(Days)
admin.site.register(ShiftType)
admin.site.register(Shift)
admin.site.register(Availability)
