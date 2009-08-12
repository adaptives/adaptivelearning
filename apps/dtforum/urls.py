from django.conf.urls.defaults import *
import dtforum.views as views

urlpatterns = patterns('',
    # Example:
    # (r'^adaptivelearnin/', include('adaptivelearning.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

		(r'^topic/questions/submit/$',views.submit_question),
		(r'^questions/$',views.get_forum_questions),
		(r'^question/submit_answer/(.*)/$',views.submit_answer),
		(r'^question/answers/(.*)/$', views.get_answers_for_question),
)
