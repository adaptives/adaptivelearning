from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from al.models import Course
from al.models import Topic

def course_list(request):
	print "user: ", request.user.username
	courses = Course.objects.all()
	return render_to_response('index.html', {'courses':courses}, context_instance=RequestContext(request))


def course_show(request, course_short_name):
	errors = []
	if(course_short_name):
		course = Course.objects.get(short_name=course_short_name)
		topics = course.topic_set.all()
		return render_to_response('course/show.html', {'course':course, 'topics':topics}, context_instance=RequestContext(request))
	else:
		errors.append("could not find any course to display")
		return render_to_response('/', {'errors':errors}, context_instance=RequestContext(request))


def course_add(request):
	
	#POST request signifies that someone is trying to add a course
	if request.method == 'POST':
		errors = []
		#add/edit the course to the db
		short_name = request.POST['short_name']
		name = request.POST['name']
		description = request.POST.get('description', '')
		if not errors:
			print "Thanks for creating a course %s - %s - %s" % (short_name, name, description)
			c = Course(short_name=short_name, name=name, description=description)
			c.save()
		return render_to_response('course/add.html', {'errors': errors}, context_instance=RequestContext(request))
	
	#GET request signifies that someone is asking for the form to add courses
	elif request.method == 'GET':
		return render_to_response('course/add.html', {}, context_instance=RequestContext(request))
	
	#We cannot process any request besides GET and POST
	else:
		print "%s requested" % (request.method)
		#error msg???


def course_edit(request, course_short_name):
	#POST request signifies that someone is trying to add a course
	if request.method == 'POST':
		#edit the course in the db
		c = None
		if 'short_name' in request.POST and request.POST['short_name']:
			try:
				c = Course.objects.get(short_name=request.POST['short_name'])
			except Course.DoesNotExist:
				print "course does not exist '%s'" % (request.POST['short_name'])
		if 'name' in request.POST and request.POST['name']:
			c.name = request.POST['name']
		c.description = request.POST.get('description', '')
		if c:
			c.save()
		t = c.topic_set.all()
		return render_to_response('course/edit.html', {'course':c, 'topics':t}, context_instance=RequestContext(request))
	
	#GET request signifies that someone is asking for the form to add courses
	elif request.method == 'GET':
		c = None
		if(course_short_name):
			c = Course.objects.get(short_name=course_short_name)
			#TODO: Get list of topics for this course and send them to the template page
			t = c.topic_set.all()
		return render_to_response('course/edit.html', {'course':c, 'topics':t}, context_instance=RequestContext(request))
	
	#We cannot process any request besides GET and POST
	else:
		print "%s requested" % (request.method)
		#error msg???


def course_manager(request):
	courses = Course.objects.all()
	return render_to_response('managecourses.html', {'courses': courses}, context_instance=RequestContext(request))


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


def topic_show(request, course_short_name, topic_id):
	#Show the requested topic
	t = Topic.objects.get(id=topic_id)
	return render_to_response('topic/show.html', {'course_short_name':course_short_name, 'topic':t}, context_instance=RequestContext(request))

def topic_add(request, course_short_name):
	#User has asked for a form to add a topic to this course
	if request.method == 'GET':
		return render_to_response('topic/add.html', {'course_short_name':course_short_name}, context_instance=RequestContext(request))
	#User has posted data to add a topic
	elif request.method == 'POST':
		t = Topic()
		t.id = None
		t.title = request.POST['title']
		t.content = request.POST['content']
		t.save()
		c = Course.objects.get(short_name=request.POST['course_short_name'])
		t.course.add(c)
		t.save()
		return render_to_response('topic/add.html', {'course_short_name':course_short_name, 'errors':['topic saved']}, context_instance=RequestContext(request))

def topic_edit(request, course_short_name, topic_id):
	#The user has asked to view topic details
	if request.method == 'GET':
		topic = Topic.objects.get(id=topic_id)
		return render_to_response('topic/edit.html', {'topic':topic, 'course_short_name':course_short_name}, context_instance=RequestContext(request))


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

def topic_delete(request, course_short_name):
	msgs = []
	errors = []
	for course_topic, on_of in request.POST.items():
		if on_of == "on":
			tokens = course_topic.split('_')
			course = Course.objects.get(short_name=tokens[0])
			topic = Topic.objects.get(id=tokens[1])
			course.topic_set.remove(topic)
	course = Course.objects.get()
	topics = course.topic_set.all()
	return render_to_response('course/edit.html', {'course':course, 'topics':topics}, context_instance=RequestContext(request))
