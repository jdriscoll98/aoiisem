from django.db import models

class Shift(models.Model):
    type = models.CharField(blank=True, max_length=100)
    hours = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.type)

class Employee(models.Model):
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    available_shifts = models.ManyToManyField(Shift, blank=True)
    number_of_scheduled_hours = models.IntegerField(blank=True, null=True)
    type_of_employee = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
