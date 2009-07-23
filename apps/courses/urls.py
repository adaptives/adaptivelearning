from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import settings
import adaptivelearning

urlpatterns = patterns('',
    # Example:
    # (r'^adaptivelearnin/', include('adaptivelearning.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

		(r'^course/show/(.*)/$', 'adaptivelearning.apps.courses.views.course_show'),
		(r'^course/topic/show/(.*)/(.*)$','adaptivelearning.apps.courses.views.topic_show'),
		(r'^course/topic/questions/submit/$','adaptivelearning.apps.courses.views.submit_question'),
		(r'^course/topic/questions/$','adaptivelearning.apps.courses.views.get_forum_questions'),
		(r'^course/question/submit_answer/(.*)/$','adaptivelearning.apps.courses.views.submit_answer'),
		(r'^course/question/answers/(.*)/$', 'adaptivelearning.apps.courses.views.get_answers_for_question'),
		(r'^manage/$', 'adaptivelearning.apps.courses.views.manage'),
		(r'^manage/courses/$', 'adaptivelearning.apps.courses.views.course_manager'),
		(r'^manage/courses/reorder/$', 'adaptivelearning.apps.courses.views.courses_reorder'),
		(r'^manage/course/$', 'adaptivelearning.apps.courses.views.course_manager'),
		(r'^manage/course/add/$', 'adaptivelearning.apps.courses.views.course_add'),
		(r'^manage/course/edit/(.*)$', 'adaptivelearning.apps.courses.views.course_edit'),
		(r'^manage/course/deletes/$', 'adaptivelearning.apps.courses.views.course_delete'),
		(r'^manage/course/topic/add/(.*)$', 'adaptivelearning.apps.courses.views.topic_add'),
		#(r'^manage/course/topic/show/$', topic_show),
		(r'^manage/course/topic/edit/(.*)/(.*)$','adaptivelearning.apps.courses.views.topic_edit'),
		(r'^manage/course/topic/edit/$', 'adaptivelearning.apps.courses.views.topic_edit_save'),
		(r'^manage/course/topic/deletes/(.*)$','adaptivelearning.apps.courses.views.topic_delete'),
		(r'^manage/course/topic/reorder/(.*)/$','adaptivelearning.apps.courses.views.topic_reorder'),
)
