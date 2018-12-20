from django.contrib import admin
from Employment.models import Employee, Manager, Clock

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def name(self, obj):
        return obj.user.first_name +  ' ' + obj.user.last_name

    name.admin_order_field = 'user__first_name'

    list_display = ('name', 'phone_number', 'email')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(Clock)
class ClockAdmin(admin.ModelAdmin):
    pass
