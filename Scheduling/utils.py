from Scheduling.models import Shift, SchedulePeriod, Availability, ShiftType
from House.models import House
import datetime
from datetime import timedelta
from django.shortcuts import render, redirect


def create_schedule(request):
    user = request.user
    if Shift.objects.all() is not None:
        current_shifts = Shift.objects.all()
        current_shifts.delete()
    house = House.objects.get(manager=user)
    scheduleperiod = SchedulePeriod.objects.get(House=house)
    date = scheduleperiod.start_date
    for i in range(30):
        print(i)
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
    return redirect('Employment:ViewSchedule')

def create_shifts(day, date, scheduleperiod, type):
    employee_list = []
    shift_date = date
    elligible_employees = Availability.objects.filter(ShiftType=type, days__day__in=[day])
    for employee in elligible_employees:
        employee_list.append(employee)
    employee_list.sort(key=lambda x: x.employee.num_hours)
    if not (Shift.objects.filter(Type=type, date=date, Employee = employee_list[0].employee).exists() or ( not
    Shift.objects.filter(Type=ShiftType.objects.get(label='Breakfast'), date=date, Employee= employee_list[0].employee).exists() and not Shift.objects.filter(Type=ShiftType.objects.get(label='Lunch'), date=date, Employee= employee_list[0].employee).exists())):
        employee = employee_list[0].employee
    else:
        employee = employee_list[1].employee
    end_date = scheduleperiod.end_date
    while shift_date <= end_date:
        shift = Shift.objects.create(
            Type = type,
            Employee = employee,
            date = shift_date
        )
        shift_date += timedelta(days=7)
    if type == 'Breakfast':
        employee.num_hours += 1
        employee.save()
    else:
        employee.num_hours += 3
        employee.save()
    return True
