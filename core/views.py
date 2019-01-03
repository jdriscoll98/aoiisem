from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate, logout as auth_logout
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from .utils import recaptcha_validation

from Employment.models import Employee, Manager
# Application Views

# Login
def login(request):
	if (request.method == "POST"):
		if True:
		# if recaptcha_validation(request.POST.get('g-recaptcha-response')):
			form = AuthenticationForm(request, request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				raw_password = form.cleaned_data.get('password')
				user = auth_authenticate(username__iexact=username, password=raw_password)
				auth_login(request, user)
				return redirect('website:homepage_view')

		else:
			raise SuspiciousOperation()
	else:
		form = AuthenticationForm()

	context = {
		'form': form,
	}
	return render(request, 'registration/login_page.html', context)

# Logout
def logout(request):
	auth_logout(request)
	next_page = request.GET.get('next', 'website:homepage_view')
	return redirect(next_page)
