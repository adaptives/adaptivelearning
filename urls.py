from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import settings
import adaptivelearning
from adaptivelearning.apps.courses.views import manage

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
		(r'^$', 'adaptivelearning.apps.courses.views.course_list'),
		(r'^registration/', 'adaptivelearning.views.register'),		
		(r'^courses/', include('adaptivelearning.apps.courses.urls')),
)
