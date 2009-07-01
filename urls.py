from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import settings
from adaptivelearning.views import manage
from al.views import course_list
from al.views import course_add
from al.views import course_manager
from al.views import course_delete
from al.views import course_show
from al.views import course_edit
from al.views import topic_add
from al.views import topic_edit
from al.views import topic_edit_save
from al.views import topic_show
from al.views import topic_delete

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^adaptivelearning/', include('adaptivelearning.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout, {'next_page':'/'}),
		(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
		(r'^$', course_list),
		(r'^course/show/(.*)/$', course_show),
		(r'^topic/show/(.*)/(.*)$',topic_show),
		(r'^manage/$', manage),
		(r'^manage/courses/$', course_manager),
		(r'^manage/course/$', course_manager),
		(r'^manage/course/add/$', course_add),
		(r'^manage/course/edit/(.*)$', course_edit),
		(r'^manage/course/deletes/$', course_delete),
		(r'^manage/course/topic/add/(.*)$', topic_add),
		#(r'^manage/course/topic/show/$', topic_show),
		(r'^manage/course/topic/edit/(.*)/(.*)$', topic_edit),
		(r'^manage/course/topic/edit/$', topic_edit_save),
		(r'^manage/course/topic/deletes/(.*)$', topic_delete),
)
