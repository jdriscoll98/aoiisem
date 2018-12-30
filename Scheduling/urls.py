from django.conf.urls import url, include
from django.urls import path
from Scheduling.views import UpdateShift, PostShift, CreateSchedulePage, PickUpVacantPage, PickUpVacant
from . import views
# Application Routes (URLs)

app_name = 'Scheduling'

urlpatterns = [
		url(r'^UpdateShift/(?P<pk>\d+)/$', UpdateShift.as_view(), name='UpdateShift'),
		url(r'^PostShift/(?P<pk>\d+)/$', PostShift.as_view(), name='PostShift'),
		url(r'^PickUpVacantShiftPage/(?P<pk>\d+)/$', PickUpVacantPage.as_view(), name='PickUpVacantPage'),
		url(r'^PickUpVacant/(?P<pk>\d+)/$', PickUpVacant.as_view(), name='PickUpVacant'),
		url(r'^CreateSchedulePage/$', CreateSchedulePage.as_view(), name='CreateSchedulePage'),
		url(r'^CreateSchedule/$', views.create_schedule, name='create_schedule'),
    	# General Page Views
]
