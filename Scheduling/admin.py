from django.contrib import admin
from Scheduling.models import Days, ShiftType, Shift, Availability, SchedulePeriod
from Scheduling.forms import AvailabilityForm

admin.site.register(Days)

@admin.register(ShiftType)
class ShiftTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(SchedulePeriod)
class SchedulePeriodAdmin(admin.ModelAdmin):
    pass

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('employee_first_name', 'Type', 'date', 'up_for_trade')
    def employee_first_name(self, obj):
        return obj.Employee.user.first_name

    employee_first_name.admin_order_field = 'Employee__user__first_name'

@admin.register(Availability)
class AvailabiltyAdmin(admin.ModelAdmin):
    pass
