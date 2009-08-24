from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import settings
import adaptivelearning
import courses
import dtforum
from courses.views import manage

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^adaptivelearnin/', include('adaptivelearning.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/admin/logout/$', logout, {'next_page':'/'}),
    (r'^admin/auth/user/admin/logout/', logout, {'next_page':'/'}),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout, {'next_page':'/'}),
    (r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^$', 'courses.views.course_list'),
		(r'^about/$', 'adaptivelearning.views.about'),
		(r'^registration/', 'adaptivelearning.views.register'),		
		(r'^terms-of-service/$', 'adaptivelearning.views.terms_of_service'),		
		(r'^privacy-policy/$', 'adaptivelearning.views.privacy_policy'),		
		(r'^profile/$', 'courses.views.user_profile'),
		(r'^profile/public/(.*)/$', 'courses.views.user_profile_public'),
		(r'^users/$', 'courses.views.list_users'),
		(r'^courses/', include('courses.urls')),
		(r'^dtforum/', include('dtforum.urls')),
		(r'^markitup/', include('markitup.urls')),
)
