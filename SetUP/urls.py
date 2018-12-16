from django.conf.urls import url, include
from django.urls import path
from . import views
from SetUP.views import RegisterHouse, SchedulePeriodForm, ShiftTypes, CurrentEmployees, SetUpComplete, BeginSetUp
# Application Routes (URLs)

app_name = 'SetUP'

urlpatterns = [
    	# Set up URLs
		url(r'^$', BeginSetUp.as_view(), name='BeginSetUp'),
		url(r'^RegisterHouse/$', RegisterHouse.as_view(), name='RegisterHouse'),
		url(r'^SchedulePeriod/$', SchedulePeriodForm.as_view(), name='SchedulePeriod'),
		url(r'^ShiftTypes/$', ShiftTypes.as_view(), name='ShiftTypes'),
		url(r'^CurrentEmployees/$', CurrentEmployees.as_view(), name='CurrentEmployees'),
		url(r'^SetUpComplete/$', SetUpComplete.as_view(), name='SetUpComplete'),

]
