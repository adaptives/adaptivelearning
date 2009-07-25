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
			user = form.save()
			#user = auth.authenticate(username=request.POST.username, password=request.POST.password1)
			#auth.login(request, user)
			#user = User.objects.get(username=request.POST['username'])
			user_profile = user.get_profile()
			if request.POST['full_name']:
				user_profile.full_name = request.POST['full_name']
			if request.POST['website']:
				user_profile.website = request.POST['website']
			if request.POST['timezone']:
				user_profile.timezone = request.POST['timezone']
			if request.POST['bio']:
				user_profile.bio = request.POST['bio']
			user_profile.save()
			return HttpResponseRedirect("/")
	else:
		form = UserCreationForm()
	return render_to_response("registration/register.html", {'form': form,})

