from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms.models import modelform_factory

from Employment.models import Manager, Employee
from Application.models import Applicant

class ManagerRequired(UserPassesTestMixin):
    def test_func(self):
        try:
            Manager.objects.get(user=self.request.user)
            return True
        except:
            return False

class EmployeeRequired(UserPassesTestMixin):
    def test_func(self):
        try:
            Employee.objects.get(user=self.request.user)
            return True
        except:
            return False

class ApplicantRequired(UserPassesTestMixin):
    def test_func(self):
        try:
            Applicant.objects.get(user=self.request.user)
            return True
        except:
            return False
class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)
