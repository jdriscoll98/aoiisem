from django.conf.urls import url, include
from django.urls import path
from Scheduling.views import UpdateShift, PostShift
# Application Routes (URLs)

app_name = 'Scheduling'

urlpatterns = [
		url(r'UpdateShift/(?P<pk>\d+)/$', UpdateShift.as_view(), name='UpdateShift'),
		url(r'PostShift/(?P<pk>\d+)/$', PostShift.as_view(), name='PostShift'),
    	# General Page Views
]
