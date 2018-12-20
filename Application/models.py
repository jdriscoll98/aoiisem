from django.db import models
from django.contrib.auth.models import User

class Applicant(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_submitted = models.DateField()
    Grade = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
#    Resume = models.FileField(upload_to='resumes', default='resumes/resume.pdf')
    statement_of_interest = models.TextField()

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)
