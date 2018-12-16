from django.conf.urls import url, include
from django.urls import path
from Employment.views import ManagerHomePage, EmployeeHomePage, SubmitAvailability
# Application Routes (URLs)

app_name = 'Employment'

urlpatterns = [
    url(r'^ManagerHomePage/$',ManagerHomePage.as_view(), name='ManagerHomePage'),
    url(r'^EmployeeHomePage/$',EmployeeHomePage.as_view(), name='EmployeeHomePage'),
    url(r'^SubmitAvailability/$',SubmitAvailability.as_view(), name='SubmitAvailability'),
    	# General Page Views
]
