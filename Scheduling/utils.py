from Scheduling.models import Shift, SchedulePeriod, Availability
from House.models import House
import datetime


def create_schedule(user):
    current_shifts = Shift.objects.all()
    current_shifts.delete()
    House = House.objects.get(manager=user)
    SchedulePeriod = SchedulePeriod.objects.get(House=House)
    date = SchedulePeriod.start_date
    for i in range(30):
        day = date.strftime('%A')
        if i  < 5:
            create_shifts(day, i, date, SchedulePeriod)
        elif i == 5:
            date = SchedulePeriod.start_date
            create_shifts(day, i, date, SchedulePeriod)
        elif i<10:
            create_shifts(day, i, date, SchedulePeriod)
        elif i == 10:
            date = SchedulePeriod.start_date
            create_shifts(day, i, date, SchedulePeriod)
        elif i < 15:
            create_shifts(day, i, date, SchedulePeriod)
        elif i == 20:
            date = SchedulePeriod
            create_shifts(day, i, date, SchedulePeriod)
        elif i < 25:
            create_shifts(day, i, date, SchedulePeriod)
        elif i == 25:
            date = SchedulePeriod.start_date
            create_shifts(day, i, date, SchedulePeriod)
        elif i < 30:
            create_shifts(day, i, date, SchedulePeriod)
    return True

def create_shifts(day, i, date, Schedule):
    employee_list = Availability.objects.filter(days__day__in=day)
    employee_list.sort(key=lambda x: x.num_hours)
    employee = employee_list[0].Employee
    shift_date = date
    if i < 5:
        type = Breakfast
    elif i < 15:
        type = Lunch
    else:
        type = Dinner

    while shift_date <= SchedulePeriod.end_date:
        Shift.create(
            Type = type,
            Employee = employee,
            date = shift_date
        )
        shift_date += timedelta(days=7)
    if type == Breakfast:
        employee.num_hours += 1
        employee.save()
    else:
        employee.num_hours += 3
        employee.save()
    date += timedelta(days=1)
    return True
