from django.contrib import admin
from website.models import Employee, AvailableShift, ScheduledShift, PostShift

admin.site.register(Employee)
admin.site.register(AvailableShift)
admin.site.register(ScheduledShift)
admin.site.register(PostShift)
