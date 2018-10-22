from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    number_of_scheduled_hours = models.IntegerField(blank=True, null=True)
    head_bus_boy = models.BooleanField(default=False)

    def get_available_shifts(self):
        return AvailableShift.filter(employee=self)

    def get_scheduled_shifts(self, day, type):
        return ScheduledShift.objects.filter(employee=self, day=day, type=type)

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
