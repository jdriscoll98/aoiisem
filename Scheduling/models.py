from django.db import models
from django.contrib.auth.models import User
from House.models import House
from Employment.models import Employee
from django.urls import reverse_lazy
from general.utils import get_default_employee

class Days(models.Model):
    day = models.CharField(max_length=10)

    def __str__(self):
        return str(self.day)

class ShiftType(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    number_of_employees = models.IntegerField()

    def get_absolute_url(self):
        return reverse_lazy('SetUP:CurrentEmployees')

    def __str__(self):
        return str(self.label)

class Shift(models.Model):
    Type = models.ForeignKey(ShiftType, on_delete=models.CASCADE)
    is_posted = models.BooleanField(default=False)
    up_for_trade = models.BooleanField(default=False)
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.Type)

class Availability(models.Model):
    ShiftType = models.ForeignKey(ShiftType, on_delete=models.CASCADE)
    days = models.ManyToManyField(Days)
    employee = models.ForeignKey(Employee, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employee) + '|' + str(self.ShiftType)

class SchedulePeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    House = models.ForeignKey(House, default=1, on_delete=models.CASCADE)
