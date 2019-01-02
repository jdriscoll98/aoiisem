from django.conf.urls import url, include
from django.urls import path
from Scheduling.views import (UpdateShift, PostShift, CreateSchedulePage,
 							PickUpVacantPage, PickUpVacant, TradeShiftPage,
							 TradeShift, PickUpPermenantShift)
from . import views
# Application Routes (URLs)

app_name = 'Scheduling'

urlpatterns = [
		url(r'^UpdateShift/(?P<pk>\d+)/$', UpdateShift.as_view(), name='UpdateShift'),
		url(r'^PostShift/(?P<pk>\d+)/$', PostShift.as_view(), name='PostShift'),
		url(r'^TradeShiftPage/(?P<pk>\d+)/$', TradeShiftPage.as_view(), name='TradeShiftPage'),
		url(r'^TradeShift/(?P<pk>\d+)/$', TradeShift.as_view(), name='TradeShift'),
		url(r'^PickUpVacantShiftPage/(?P<pk>\d+)/$', PickUpVacantPage.as_view(), name='PickUpVacantPage'),
		url(r'^PickUpPermenantShift/(?P<pk>\d+)/$', PickUpPermenantShift.as_view(), name='PickUpPermenantShift'),
		url(r'^PickUpVacant/(?P<pk>\d+)/$', PickUpVacant.as_view(), name='PickUpVacant'),
		url(r'^CreateSchedulePage/$', CreateSchedulePage.as_view(), name='CreateSchedulePage'),
		url(r'^CreateSchedule/$', views.create_schedule, name='create_schedule'),
    	# General Page Views
]
