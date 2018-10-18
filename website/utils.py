from .models import Employee, ScheduledShift

def get_employees(user_id):
    return Employee.objects.get(user_id=user_id)

def get_shifts(user_id):
    employee = Employee.objects.get(user_id=user_id)
    return ScheduledShift.objects.filter(employee=employee)
