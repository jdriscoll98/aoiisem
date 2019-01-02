from django.conf.urls import url, include
from django.urls import path
from Employment.views import (ManagerHomePage, EmployeeHomePage, SubmitAvailability,
                                EmployeeUpdate, ClockView, EmployeeDetails, ViewSchedule, DownloadTimeSheet )
from . import views

# Application Routes (URLs)

app_name = 'Employment'

urlpatterns = [
    url(r'^ManagerHomePage/$',ManagerHomePage.as_view(), name='ManagerHomePage'),
    url(r'^EmployeeHomePage/$',EmployeeHomePage.as_view(), name='EmployeeHomePage'),
    url(r'^EmployeeDetails/(?P<pk>\d+)/$',EmployeeDetails.as_view(), name='EmployeeDetails'),
    url(r'^ViewSchedule/$',ViewSchedule.as_view(), name='ViewSchedule'),
    url(r'^Clock/$',ClockView.as_view(), name='Clock'),
    url(r'^DownloadTimeSheet/$', views.DownloadTimeSheet, name='DownloadTimeSheet'),
    url(r'^SubmitAvailability/$',SubmitAvailability.as_view(), name='SubmitAvailability'),
    url(r'^EmployeeUpdate/(?P<pk>\d+)/$', EmployeeUpdate.as_view(), name='EmployeeUpdate'),
    	# General Page Views
]
