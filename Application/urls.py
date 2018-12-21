from django.conf.urls import url, include
from django.urls import path
from Application.views import (NewApplication, ApplicationHomePage, UpdateApplication,
 ApplicantDetails, AcceptApplicant, DeleteApplicant)
# Application Routes (URLs)

app_name = 'Application'

urlpatterns = [
		url(r'^NewApplication/$', NewApplication.as_view(), name='NewApplicationPage'),
		url(r'^ApplicationHomePage/$', ApplicationHomePage.as_view(), name='ApplicationHomePage'),
		url(r'^UpdateApplication/(?P<pk>\d+)/$', UpdateApplication.as_view(), name='UpdateApplication'),
		url(r'^ApplicantDetails/(?P<pk>\d+)/$', ApplicantDetails.as_view(), name='ApplicantDetails'),
		url(r'^AcceptApplicant/(?P<pk>\d+)/$', AcceptApplicant.as_view(), name='AcceptApplicant'),
		url(r'^DeleteApplicant/(?P<pk>\d+)/$',DeleteApplicant.as_view(), name='DeleteApplicant'),
    	# General Page Views
]
