from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from . import views

# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
    	# General Page Views
		url('^login/$', LoginView.as_view(template_name='registration/login_page.html'), name="login"),
		url('^logout/$', LogoutView.as_view(template_name='registration/login_page.html'), name="logout"),
	    url(r'^admin/', admin.site.urls),
		url(r'^$', views.homepage_view, name='homepage_view'),
]
