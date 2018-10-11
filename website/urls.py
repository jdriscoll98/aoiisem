from django.conf.urls import url, include
from django.urls import path
from .views import request_time_off_page_view
from . import views
# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
    	# General Page Views
		url(r'^$', views.homepage_view, name='homepage_view'),
		url(r'^request-time-off$', views.request_time_off_page_view, name='RequestTimeOffPageView'),
]
