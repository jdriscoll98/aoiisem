from Employment.models import Clock
from datetime import timedelta, datetime
import datetime

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
