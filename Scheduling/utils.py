from Scheduling.models import Shift, SchedulePeriod, Availability, ShiftType
from House.models import House
from Employment.models import Employee
import datetime
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.models import User



def create_schedule(request):
    user = request.user
    if Shift.objects.all() is not None:
        current_shifts = Shift.objects.all()
        current_shifts.delete()
    house = House.objects.get(manager=user)
    scheduleperiod = SchedulePeriod.objects.get(House=house)
    date = scheduleperiod.start_date
    for employee in Employee.objects.all():
        employee.num_hours = 0
        employee.save()
    for i in range(30):
        day = date.strftime('%A')
        if i  < 5:
            type = ShiftType.objects.get(label='Breakfast')
            create_shifts(day, date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i == 5:
            type = ShiftType.objects.get(label='Lunch')
            date = scheduleperiod.start_date
            day = date.strftime('%A')
            create_shifts(day, date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i<10:
            type = ShiftType.objects.get(label='Lunch')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i == 10:
            type = ShiftType.objects.get(label='Lunch')
            date = scheduleperiod.start_date
            day = date.strftime('%A')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i < 15:
            type = ShiftType.objects.get(label='Lunch')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i == 15:
            type = ShiftType.objects.get(label='Dinner')
            date = scheduleperiod.start_date
            day = date.strftime('%A')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i < 20:
            type = ShiftType.objects.get(label='Dinner')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i == 20:
            type = ShiftType.objects.get(label='Dinner')
            date = scheduleperiod.start_date
            day = date.strftime('%A')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i < 25:
            type = ShiftType.objects.get(label='Dinner')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i == 25:
            type = ShiftType.objects.get(label='Dinner')
            date = scheduleperiod.start_date
            day = date.strftime('%A')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
        elif i<30:
            type = ShiftType.objects.get(label='Dinner')
            create_shifts(day,  date, scheduleperiod, type)
            date = date + timedelta(days=1)
    default_user = User.objects.get(username='default')
    default = Employee.objects.get(user=default_user)
    for shift in Shift.objects.exclude(Employee=default):
        date = shift.date
        shift_date = date + timedelta(7)
        end_date = scheduleperiod.end_date
        while shift_date < end_date:
            shift = Shift.objects.create(
                Type = shift.Type,
                Employee = shift.Employee,
                date = shift_date
            )
            shift_date += timedelta(7)
    return redirect('Employment:ViewSchedule')

def create_shifts(day, date, scheduleperiod, type):
    employee_list = []
    shift_date = date
    elligible_employees = Availability.objects.filter(ShiftType=type, days__day__in=[day])
    for employee in elligible_employees:
        employee_list.append(employee)
    employee_list.sort(key=lambda x: x.employee.num_hours)
    employee = get_employee(employee_list, type, day, date, scheduleperiod)
    shift = Shift.objects.create(
        Type = type,
        Employee = employee,
        date = shift_date
    )
    if type == 'Breakfast':
        employee.num_hours += 1
        employee.save()
    else:
        employee.num_hours += 3
        employee.save()
    return True

def get_already_scheduled(type, date, employee):
    if (Shift.objects.filter(Type=type, date=date, Employee = employee).exists()):
        return False
    else:
        return True

def get_triple_shift(date, employee):
    if (Shift.objects.filter(Type=ShiftType.objects.get(label='Breakfast'), date=date, Employee= employee).exists()
    and Shift.objects.filter(Type=ShiftType.objects.get(label='Lunch'), date=date, Employee= employee).exists()):
        return False
    else:
        return True

def get_employee(employee_list, type, day, date, scheduleperiod):
    try:
        employee = employee_list[0].employee
    except:
        employee = Employee.objects.get(user=User.objects.get(username='default'))
    if (employee.user.username != 'default') and len(employee_list) >= 2:
        if get_already_scheduled(type, date, employee) and get_triple_shift(date, employee):
            employee = employee_list[0].employee
        elif get_already_scheduled(type, date, employee_list[1].employee) and get_triple_shift(date, employee_list[1].employee):
            employee = employee_list[1].employee
        else:
            try:
                employee = employee_list[2].employee
            except:
                employee = Employee.objects.get(user=User.objects.get(username='default'))
    else:
        if (employee.user.username != 'default') and get_already_scheduled(type, date, employee) and get_triple_shift(date, employee):
            employee = employee_list[0].employee
        else:
            employee = Employee.objects.get(user=User.objects.get(username='default'))
    return employee
