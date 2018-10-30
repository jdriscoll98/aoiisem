from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    head_bus_boy = models.BooleanField(default=False)

    def get_number_of_hours(self):
        hours = 0
        for shift in ScheduledShift.objects.filter(employee=self):
            if shift.type == "Breakfast":
                hours += 1
            else:
                hours += 3
        return hours

    def get_available_shifts(self):
        return AvailableShift.filter(employee=self)

    def get_scheduled_shifts(self, day, type):
        try:
            return ScheduledShift.objects.get(employee=self, day=day, type=type)
        except:
            return None

    def __str__(self):
        return str(self.name)

class AvailableShift(models.Model):
    DAYS= (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    )
    TYPES=(
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner')
    )
    day = models.CharField(max_length = 100, blank=True, choices=DAYS)
    type = models.CharField(max_length=100, blank=True, choices=TYPES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return  str(self.employee) + " " + str(self.day) + " " + str(self.type)

class ScheduledShift(models.Model):
    DAYS= (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    )
    TYPES=(
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner')
    )
    day = models.CharField(max_length = 100, blank=True, choices=DAYS)
    type = models.CharField(max_length=100, blank=True, choices=TYPES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return  str(self.employee) + " | " + str(self.day) + " " + str(self.type)

class PostShift(models.Model):
    DAYS= (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    )
    TYPES=(
    ('Breakfast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner')
    )
    day = models.CharField(max_length = 100, choices=DAYS)
    type = models.CharField(max_length=100, choices=TYPES)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return  str(self.employee) + " | " + str(self.day) + " " + str(self.type)
