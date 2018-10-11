from django.conf.urls import url, include
from django.urls import path
from .views import request_time_off_page_view, request_time_off_form_view, shifts_available_page_view
from . import views
# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
    	# General Page Views
		url(r'^$', views.homepage_view, name='homepage_view'),
		url(r'^request-time-off$', views.request_time_off_page_view, name='RequestTimeOffPageView'),
		url(r'^request-time-off-form$', views.request_time_off_form_view, name='RequestTimeOffFormView'),
		url(r'^shifts-available$', views.shifts_available_page_view, name='ShiftsAvailableView'),
]
