from django.contrib import admin
from website.models import Employee, AvailableShift, ScheduledShift

admin.site.register(Employee)
admin.site.register(AvailableShift)
admin.site.register(ScheduledShift)
