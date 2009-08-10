import logging
import datetime
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import Serializer as JSONSerializer 
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from apps.courses.models import Course
from apps.courses.models import Topic
from apps.courses.models import TopicOrder
from apps.courses.models import CourseOrder
from apps.courses.models import Forum
from apps.courses.models import Question
from apps.courses.models import Answer

class DateModifyingEncoder(DjangoJSONEncoder):
	SECONDS_IN_DAY = 60 * 60 * 24
	SECONDS_IN_HR = 60 * 60
	SECONDS_IN_MIN = 60
	def default(self, object):
		#format =  "%d %b %Y, %H:%M"
		if isinstance(object, datetime.datetime):
			delta = datetime.datetime.utcnow() - object
			return self.get_delta_as_string(delta)
		else:
			return super(DateModifyingEncoder, self).default(object)

	def get_delta_as_string(self, delta):
		days = delta.days
		seconds = delta.seconds
		hours = 0
		minutes = 0
		hours = seconds / self.SECONDS_IN_HR
		seconds = seconds % self.SECONDS_IN_HR
		minutes = seconds / self.SECONDS_IN_MIN 
		seconds = seconds % self.SECONDS_IN_MIN
		delta_str = ''
		if days > 0:
			delta_str += str(days) + ' days, '
		if hours > 0:
			delta_str += str(hours) + ' hours, '
		if days <= 0 and seconds > 0:
			delta_str += str(seconds) + ' secs, '
		return delta_str


class DateModifyingJSONSerializer(JSONSerializer):
	def end_serialization(self):
		self.options.pop('stream', None)
		self.options.pop('fields', None)	
		simplejson.dump(self.objects, self.stream, cls=DateModifyingEncoder, **self.options)


def course_list(request):
	logging.info('landing page invoked')
	courses = get_sorted_courses()
	return render_to_response('index.html', {'courses':courses}, context_instance=RequestContext(request))


def course_show(request, course_short_name):
	errors = []
	if(course_short_name):
		course = Course.objects.get(short_name=course_short_name)
		topics = get_sorted_topics(course)
		return render_to_response('course/show.html', {'course':course, 'topics':topics}, context_instance=RequestContext(request))
	else:
		errors.append("could not find any course to display")
		return render_to_response('/', {'errors':errors}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def course_add(request):
	
	#POST request signifies that someone is trying to add a course
	if request.method == 'POST':
		errors = []
		#add/edit the course to the db
		short_name = request.POST['short_name']
		name = request.POST['name']
		description = request.POST.get('description', '')
		c = Course(short_name=short_name, name=name, description=description)
		c.save()
		try:
			course_order = CourseOrder.objects.get(course=c)
		except CourseOrder.DoesNotExist:
			course_order = CourseOrder(course=c)
			course_orders = CourseOrder.objects.order_by('-order')[:1]
			if course_orders:
				course_order.order = course_orders[0].order + 1
			else:
				course_order.order=0
		course_order.save()
		return render_to_response('course/add.html', {'errors': errors}, context_instance=RequestContext(request))
	
	#GET request signifies that someone is asking for the form to add courses
	elif request.method == 'GET':
		return render_to_response('course/add.html', {}, context_instance=RequestContext(request))
	
	#We cannot process any request besides GET and POST
	else:
		logging.error("%s requested" % (request.method))
		#error msg???


@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def course_edit(request, course_short_name):
	#POST request signifies that someone is trying to add a course
	if request.method == 'POST':
		#edit the course in the db
		c = None
		if 'short_name' in request.POST and request.POST['short_name']:
			try:
				c = Course.objects.get(short_name=request.POST['short_name'])
			except Course.DoesNotExist:
				logging.error("course does not exist '%s'" % (request.POST['short_name']))
		if 'name' in request.POST and request.POST['name']:
			c.name = request.POST['name']
		c.description = request.POST.get('description', '')
		if c:
			c.save()
		t = c.topic_set.all()
		sorted_topics = get_sorted_topics(c)
		#if t.size() > sorted_topics.size():
		#	sorted_topics = t
		return render_to_response('course/edit.html', {'course':c, 'topics':sorted_topics}, context_instance=RequestContext(request))
	
	#GET request signifies that someone is asking for the form to add courses
	elif request.method == 'GET':
		c = None
		if(course_short_name):
			c = Course.objects.get(short_name=course_short_name)
			#TODO: Get list of topics for this course and send them to the template page
			t = c.topic_set.all()
			sorted_topics = get_sorted_topics(c)
		return render_to_response('course/edit.html', {'course':c, 'topics':sorted_topics}, context_instance=RequestContext(request))
	
	#We cannot process any request besides GET and POST
	else:
		logging.error("%s requested" % (request.method))
		#error msg???


@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def manage(request):
	return render_to_response('manage.html', context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def course_manager(request):
	courses = get_sorted_courses()
	return render_to_response('managecourses.html', {'courses': courses}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def course_delete(request):
	msgs = []
	errors = []
	for course_short_name, on_of in request.POST.items():
		if on_of == "on":
			c = Course.objects.get(short_name=course_short_name)
			if c:
				c.delete()
	courses = Course.objects.all()
	return render_to_response('managecourses.html', {'msgs':msgs, 'courses':courses, 'errors':errors}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def courses_reorder(request):
	course_short_names = request.POST['order'].split(',')
	msg = ''
	count = 0
	for course_short_name in course_short_names:
		count += 1
		if(course_short_name == ''):
			continue
		try:
			course = Course.objects.get(short_name=course_short_name)
			try:
				co = CourseOrder.objects.get(course=course)
			except:
				co = CourseOrder(course=course, order=count)
			co.order = count
			co.save()
			msg = 'Course reordering complete'
		except Exception, e:
			logging.error("Could not reorder courses " + e)
			msg = 'Course reordering faile ', e
	return HttpResponse(msg)

def topic_show(request, course_short_name, topic_id):
	#Show the requested topic
	t = Topic.objects.get(id=topic_id)
	return render_to_response('topic/show.html', {'course_short_name':course_short_name, 'topic':t}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def topic_reorder(request, course_short_name):
	msg = ''
	topic_ids = request.POST['order'].split(',')
	count = 0
	for topic_id in topic_ids:
		count += 1
		if topic_id == '':
			continue
		try:
			course = Course.objects.get(short_name = course_short_name)
			topic = Topic.objects.get(id = int(topic_id))
			to = None
			try:
				to = TopicOrder.objects.get(course=course, topic=topic)
			except:
				to = TopicOrder(course=course, topic=topic, order=count)
			to.order = count
			#(to, created) = TopicOrder.objects.get_or_create(course=course, topic=topic)
			to.save()
			msg = 'Topic ordering successfull'
		except Exception, x:
			logging.error("could not save TopicOrder object " + x)
			msg = 'Topic ordering failed because ' + x
	return HttpResponse(msg);
	

@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def topic_add(request, course_short_name):
	#User has asked for a form to add a topic to this course
	if request.method == 'GET':
		return render_to_response('topic/add.html', {'course_short_name':course_short_name}, context_instance=RequestContext(request))
	#User has posted data to add a topic
	elif request.method == 'POST':
		t = Topic()
		t.title = request.POST['title']
		t.content = request.POST['content']
		c = Course.objects.get(short_name=request.POST['course_short_name'])
		t.course = c
		t.save()
		topic_order = TopicOrder(course=c, topic=t)
		topic_orders = TopicOrder.objects.filter(course=c).order_by('-order')[:1]
		if topic_orders:
			topic_order.order = topic_orders[0].order + 1
		else:
			topic_order.order = 0
		topic_order.save()
		forum_url = "/courses/course/topic/show/"+c.short_name+"/"+str(t.pk)
		forum = Forum(url=forum_url)
		forum.save()
		return render_to_response('topic/add.html', {'course_short_name':course_short_name, 'errors':['topic saved']}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def topic_edit(request, course_short_name, topic_id):
	#The user has asked to view topic details
	if request.method == 'GET':
		topic = Topic.objects.get(id=topic_id)
		return render_to_response('topic/edit.html', {'topic':topic, 'course_short_name':course_short_name}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def topic_edit_save(request):
	#The user has posted data to edit a course's topic
	if request.method == 'POST':
		topic_id = request.POST['topic_id']
		topic = Topic.objects.get(id=topic_id)
		topic.title = request.POST['title']
		topic.content = request.POST['content']
		topic.save()
		course = Course.objects.get(short_name=request.POST['course_short_name'])
		topics = course.topic_set.all()
		return render_to_response('course/edit.html', {'course':course, 'topics':topics}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff, "/accounts/login/")
def topic_delete(request, course_short_name):
	msgs = []
	errors = []
	for course_topic, on_of in request.POST.items():
		if on_of == "on":
			tokens = course_topic.split('_')
			course = Course.objects.get(short_name=tokens[0])
			topic = Topic.objects.get(id=tokens[1])
			topic.delete()
	course = Course.objects.get(short_name=course_short_name)
	topics = course.topic_set.all()
	return render_to_response('course/edit.html', {'course':course, 'topics':topics}, context_instance=RequestContext(request))

def get_forum_questions(request):
	res = ''
	if request.method == 'GET':
		forum_url = request.GET['url']
		try:
			forum = Forum.objects.select_related().get(url=forum_url)
			questions = forum.questions.all()
			res = get_date_formatted_json(questions)
			return HttpResponse(res, mimetype="application/javascript")
		except Exception, e:
			print "Could not get questions ", e
			logging.error("Error: Could not process request: " + e)
			res = "[{'error':'Could not process request'}]"
	else:
		res = "[{'error':'Could not process request'}]"
		return HttpResponse(res)

@user_passes_test(lambda u: u.is_authenticated(), "/accounts/login/")
def submit_question(request):
	res = ''
	if request.method == 'POST':
		try:
			url = request.POST['url']
			title = request.POST['title']
			text = request.POST['question']
			forum = Forum.objects.get(url=url)
			questionModel = Question()
			questionModel.forum = forum
			questionModel.title = title
			questionModel.text = text
			questionModel.user = request.user
			questionModel.save()
			return HttpResponse(res)
		except Exception, e:
			msg = "Could not save question because: " +  e
			logging.error(msg)
			res = "[{'error':" + msg + "}]"
			return HttpResponse(res)
	else:
		msg = "Could not process request for method " + request.method
		res = "[{'error':'Could not process request method'" + request.method + "}]"
		return HttpResponse(res)


def get_answers_for_question(request, question_id):
	try:
		question = Question.objects.get(pk=int(question_id))
		answers = question.answers.all()
		res = get_date_formatted_json(answers)
		return HttpResponse(res, mimetype="application/javascript")
	except Exception, e:
		logging.error("Could not process request because: " + e)
		return HttpResponse("[{'error':'Could not process request'}]")


@user_passes_test(lambda u: u.is_authenticated(), "/accounts/login/")
def submit_answer(request, question_id):
	try:
		answer_text = request.POST['answer']
		if not answer_text:
			return HttpResponse('Cannot save empty answer')
		question = Question.objects.get(pk=int(question_id))
		answer = Answer(text=answer_text)
		answer.question = question
		answer.user = request.user
		answer.save()
		return HttpResponse('Thanks')
	except Exception, e:
		logging.error('answer could not be saved: ' + e)
		return HttpResponse('Sorry but your answer could not be processed')

@user_passes_test(lambda u: u.is_authenticated(), "/accounts/login/")
def user_profile(request):
	errors = []
	if request.method == 'GET':
		users_questions = Question.objects.filter(user__username=request.user.username)
		users_answers = Answer.objects.filter(user__username=request.user.username)
		return render_to_response('user_profile.html', {'questions':users_questions, 'answers':users_answers}, context_instance=RequestContext(request))
	elif request.method == 'POST':
		try:
			user = User.objects.get(username=request.POST['username'])
			user_profile = user.get_profile()
			if request.POST['password1'] or request.POST['password2']:
				if request.POST['password1'] == request.POST['password2']:
					user.set_password(request.POST['password1'])
					try:
						user.save()
					except Exception, e:
						errors.append("Could not change password " + e)
				else:
					errors.append('password does not match retyped password')
			if request.POST['full_name']:
				user_profile.full_name = request.POST['full_name']
			if request.POST['website']:
				user_profile.website = request.POST['website']
			if request.POST['timezone']:
				user_profile.timezone = request.POST['timezone']
			if request.POST['bio']:
				user_profile.bio = request.POST['bio']
			user_profile.save()
		except Exception, e:
			logging.error("Exception occured while saving user_profile " + e)
			errors.append(str(e))
		return render_to_response('user_profile.html', {'errors': errors}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_authenticated(), "/accounts/login/")
def user_profile_public(request, username):
	if request.method == 'GET':
		users_questions = Question.objects.filter(user__username=username)
		users_answers = Answer.objects.filter(user__username=username)
		profiled_user = User.objects.get(username=username)
		return render_to_response('user_profile_public.html', {'profiled_user':profiled_user, 'questions':users_questions, 'answers':users_answers}, context_instance=RequestContext(request))
			

@user_passes_test(lambda u: u.is_authenticated(), "/accounts/login/")
def list_users(request):
	if request.method == 'GET':
		#List all users except the root user
		users = User.objects.exclude(is_superuser = True)
		return render_to_response('users.html', {'users':users}, context_instance=RequestContext(request))
			
def get_sorted_courses():
	course_orders = CourseOrder.objects.all()
	course_order_list = list(course_orders)
	course_order_list.sort(lambda x, y: cmp(x.order, y.order))
	sorted_courses = [course_order.course for course_order in course_order_list]
	return sorted_courses

def get_sorted_topics(course):
	topic_orders = TopicOrder.objects.filter(course=course)
	topic_order_list = list(topic_orders)
	topic_order_list.sort(lambda x, y:  cmp(x.order,y.order))
	sorted_topics = [topic_order.topic for topic_order in topic_order_list]
	return sorted_topics

def get_date_formatted_json(query_set):
	#current_date_format = DjangoJSONEncoder.DATE_FORMAT
	#current_time_format = DjangoJSONEncoder.TIME_FORMAT
	#DjangoJSONEncoder.DATE_FORMAT = "%d %b %Y,"			
	#DjangoJSONEncoder.TIME_FORMAT = "%H:%M"
	json_serializer = DateModifyingJSONSerializer() # serializers.get_serializer("json")()
	res = json_serializer.serialize(query_set)
	#res = serializers.serialize("json", query_set, cls=DateModifyingEncoder)
	#DjangoJSONEncoder.DATE_FORMAT = current_date_format			
	#DjangoJSONEncoder.TIME_FORMAT = current_time_format
	return res

