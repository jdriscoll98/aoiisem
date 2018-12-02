from django.db import models
from django.contrib.auth.models import User
from House.models import House
from Employment.models import Employee

class Days(models.Model):
    day = models.CharField(max_length=8)

class ShiftType(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    number_of_employees = models.IntegerField()

class Shift(models.Model):
    Type = models.ForeignKey(ShiftType, on_delete=models.CASCADE)
    up_for_trade = models.BooleanField(default=False)
    Employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    date = models.DateField()

class Availability(models.Model):
    ShiftType = models.ForeignKey(ShiftType, on_delete=models.CASCADE)
    days = models.ManyToManyField(Days)
