from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Applicant(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    date_submitted = models.DateField()
    Grade = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    Resume = models.FileField(upload_to='resumes', default='resumes/resume.pdf')
    statement_of_interest = models.TextField()
    old = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)
