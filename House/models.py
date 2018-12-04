from django.db import models
from django.contrib.auth.models import User

#----------------------------------------

class House(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
