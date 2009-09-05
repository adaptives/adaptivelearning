import traceback
import sys
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template import loader, Context
from django.shortcuts import render_to_response
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from courses.models import UserProfile

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

def style(request, file_name):

	from themes.skyish import theme

	body = {'color':theme['body_fg'],
					'background':theme['body_bg'],
					'font_family':'''Georgia, "Times New Roman", serif, "Helvetica Neue", Helvetica, Arial, sans-serif'''}

	header = {'background':theme['header_bg'] + ' none repeat scroll 0 0',
						'border_bottom':'1px solid ' + theme['header_bottom_border'],
						'nav_main__background_color':theme['nav_main_bg'],
						'nav_main__color':theme['nav_main_fg'],
						'nav_main__border_top':'1px solid ' + theme['nav_main_border_top'],
						'nav_main__font_family':""""Helvetica Neue",Helvetica,Arial,sans-serif""",
						'nav_main__a_visited_color':theme['nav_main_a_visited'],
						'nav_main__a_link_color':theme['nav_main_a_link'],
						'nav_main__a_hover_color':theme['nav_main_a_hover']}

	h2 = {'color':theme['h2_color'],
				'font_size':'1.3em',
				'main_width':'70%',}

	content = {'width':'1024px',
						'main__width':'70%',
						'sidebar__width':'27%',
						'sidebar__min_height':'750px',
						'sidebar__background_image':"url(\'/site-media/images/blueLinesGradient-1068x577.jpg\')",
						'sidebar__a_hover_color':theme['sidebar_a_hover']}

	footer = {'color':theme['footer_fg'],
						'background_color':theme['footer_bg'],
						'width':'1024px',
						'a_link__color':theme['footer_a_link'],
						'a_link__font_size':'11px',
						'a_visited__color':theme['footer_a_visited'],
						'a_visited__font_size':'11px',
						'a_hover__color':theme['footer_a_hover'],
						'a_hover__font_size':'11px'}

	course_details = {'border_bottom':'1px dotted ' + theme['course_details_bottom_border']}

	course_listing = {'a_link__color':theme['course_listing_a_link'],
										'a_visited__color':theme['course_listing_a_visited'],
										'a_hover__color':theme['course_listing_a_hover']}

	course_name = {'color':theme['course_name']}
	topic_name = {'color':theme['topic_name']}

	course_description = {'a_visited__color':theme['course_description_a_visited'],
												'a_link__color':theme['course_description_a_link'],
												'a_hover__color':theme['course_description_a_hover']}

	course_topics = {'a_link__color':theme['course_topics_a_link'],
									'a_visited__color':theme['course_topics_a_visited'],
									'a_hover__color':theme['course_topics_a_hover']}

	link_theme_b = {'a_link__color':theme['link_theme_b_a_link'],
									'a_visited__color':theme['link_theme_b_a_link'],
									'a_hover__color':theme['link_theme_b_a_link']}

	a = {'link_color':theme['a_link'],
			 'visited_color':theme['a_visited']}

	template = loader.get_template('style-django.tml')
	context = Context({'body':body,
										'header':header,
										'content':content,
										'h2':h2,
										'footer':footer,
										'course_details':course_details,
										'course_listing':course_listing,
										'course_name':course_name,
										'topic_name':topic_name,
										'course_description':course_description,
										'course_topics':course_topics,
										'link_theme_b':link_theme_b,
										'a':a})
	css = template.render(context)
	return HttpResponse(css, mimetype="text/css")
