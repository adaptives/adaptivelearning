from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth 

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			#user = auth.authenticate(username=request.POST.username, password=request.POST.password1)
			#auth.login(request, user)
			return HttpResponseRedirect("/")
	else:
		form = UserCreationForm()
	return render_to_response("registration/register.html", {'form': form,})

