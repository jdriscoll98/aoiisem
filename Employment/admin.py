from django.contrib import admin
from Employment.models import Employee, Manager

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass
