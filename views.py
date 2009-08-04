import traceback
import sys
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from adaptivelearning.apps.courses.models import UserProfile

class UserProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('full_name', 'email', 'website', 'timezone', 'bio')
		
def register(request):
	if request.method == 'POST':
		try:
			user_form = UserCreationForm(request.POST)
			user_profile_form = UserProfileForm(request.POST)
			if user_form.is_valid() and user_profile_form.is_valid():
				user = user_form.save()
				user_profile = UserProfile()
				user_profile.full_name = request.POST['full_name']
				user_profile.email = request.POST['email']
				user_profile.website = request.POST['website']
				user_profile.email = request.POST['timezone']
				user_profile.email = request.POST['bio']
				user_profile.user = user
				user_profile.save()
				#user_profile_tmp = user.get_profile()
				#user_profile = user_profile_form.save(commit=False)
				#user_profile.user = user_profile_tmp.user
				#user_profile.save()
				return HttpResponseRedirect("/")
			else:
				return render_to_response("registration/register.html", {'user_form': user_form, 'user_profile_form':user_profile_form})
		except Exception, e:
			logging.error("could not save UserProfile: " + e)
			return render_to_response("registration/register.html")
	else:
		user_form = UserCreationForm()
		user_profile_form = UserProfileForm()
		return render_to_response("registration/register.html", {'user_form': user_form, 'user_profile_form':user_profile_form})


def about(request):
	return render_to_response("about.html", context_instance=RequestContext(request))


def terms_of_service(request):
	return render_to_response("terms_of_service.html", context_instance=RequestContext(request))


def privacy_policy(request):
	return render_to_response("privacy_policy.html", context_instance=RequestContext(request))
