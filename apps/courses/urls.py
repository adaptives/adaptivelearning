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

		(r'^course/show/(.*)/$', 'courses.views.course_show'),
		(r'^course/topic/show/(.*)/(.*)$','courses.views.topic_show'),
		(r'^course/topic/questions/submit/$','courses.views.submit_question'),
		(r'^course/topic/questions/$','courses.views.get_forum_questions'),
		(r'^course/question/submit_answer/(.*)/$','courses.views.submit_answer'),
		(r'^course/question/answers/(.*)/$', 'courses.views.get_answers_for_question'),
		(r'^manage/$', 'courses.views.manage'),
		(r'^manage/courses/$', 'courses.views.course_manager'),
		(r'^manage/courses/reorder/$', 'courses.views.courses_reorder'),
		(r'^manage/course/$', 'courses.views.course_manager'),
		(r'^manage/course/add/$', 'courses.views.course_add'),
		(r'^manage/course/edit/(.*)$', 'courses.views.course_edit'),
		(r'^manage/course/deletes/$', 'courses.views.course_delete'),
		(r'^manage/course/topic/add/(.*)$', 'courses.views.topic_add'),
		#(r'^manage/course/topic/show/$', topic_show),
		(r'^manage/course/topic/edit/(.*)/(.*)$','courses.views.topic_edit'),
		(r'^manage/course/topic/edit/$', 'courses.views.topic_edit_save'),
		(r'^manage/course/topic/deletes/(.*)$','courses.views.topic_delete'),
		(r'^manage/course/topic/reorder/(.*)/$','courses.views.topic_reorder'),
)
