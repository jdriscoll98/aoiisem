from django.conf.urls import url, include
from django.urls import path
from Scheduling.views import PickUpShift
# Application Routes (URLs)

app_name = 'Scheduling'

urlpatterns = [
		url(r'^PickUpShift/(?P<pk>\d+)/$', PickUpShift.as_view(), name='PickUpShift'),
    	# General Page Views
]
