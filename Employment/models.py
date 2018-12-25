from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField()
    pay_rate = models.IntegerField()
    Employee_Number = models.IntegerField()
    clocked_in = models.BooleanField(default=False)
    min_hours = models.IntegerField(default=0)
    max_hours = models.IntegerField(default=0)
    num_hours = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return str(self.name)

class Clock(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time = models.TimeField()
    day = models.DateField()

    def __str__(self):
        return str(self.employee) + ' | ' + str(self.day) + ' | ' + str(self.time)
