from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
    	# General Page Views
		url(r'^login/$', auth_views.login, name='login'),
	    url(r'^logout/$', auth_views.logout, name='logout'),
	    url(r'^admin/', admin.site.urls),
		url(r'^$', views.homepage_view, name='homepage_view'),
]
