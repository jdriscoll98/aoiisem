from django.conf.urls import url, include
from django.urls import path
from Application.views import NewApplication, ApplicationHomePage, UpdateApplication
# Application Routes (URLs)

app_name = 'Application'

urlpatterns = [
		url(r'^NewApplication/$', NewApplication.as_view(), name='NewApplicationPage'),
		url(r'^ApplicationHomePage/$', ApplicationHomePage.as_view(), name='ApplicationHomePage'),
		url(r'^UpdateApplication/(?P<pk>\d+)/$', UpdateApplication.as_view(), name='UpdateApplication'),
    	# General Page Views
]
