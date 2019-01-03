from Employment.models import Clock, Employee
from datetime import timedelta, datetime
import datetime
from django.http import HttpResponse
import csv


def export_timesheet_data():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aoiitimesheet.csv"'
    writer = csv.writer(response)
    employee_list = Employee.objects.all().exclude(Employee_Number=0000).order_by('user')
    for employee in employee_list:
        total_hours = get_total_hours(employee)
        try:
            clock_in = Clock.objects.filter(in_out = 'in', employee=employee)
            in_data = ['IN']
            for time in clock_in:
                in_data.append(time.time.strftime('%H:%M:%S'))
        except:
            clock_in = []
        try:
            clock_out = Clock.objects.filter(in_out = 'out', employee=employee)
            out_data = ['OUT']
            for time in clock_out:
                out_data.append(time.time.strftime('%H:%M:%S'))
        except:
            clock_out = []
        writer.writerow([employee])
        writer.writerow(in_data)
        writer.writerow(out_data)
        writer.writerow(['Total:', total_hours])
        writer.writerow(' ')
    return response

def get_total_hours(employee):
    clocks = Clock.objects.filter(employee=employee)
    total_time = 0
    for i, clock in enumerate(clocks):
        print(clock)
        if i != (len(clocks) - 1):
            if (i % 2 == 0):
                time = clocks[i+1].time - clocks[i].time
                print(time)
                total_time += time.seconds
    return str(total_time / 3600) + ' hours'
