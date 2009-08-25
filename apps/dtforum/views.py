import logging
import datetime
from django import forms
from django.utils.html import strip_tags
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import Serializer as JSONSerializer 
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from dtforum.models import Forum
from dtforum.models import Question
from dtforum.models import Answer
from markitup.widgets import MarkItUpWidget
from django.forms.widgets import TextInput
from markdown import markdown

class QuestionForm(forms.Form):
	title = forms.CharField(max_length=128, widget=TextInput(attrs={'size':"60", 'class':'markItUpEditor'}))
	contents = forms.CharField(widget=MarkItUpWidget(attrs={'cols':'80'}))

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



def get_forum_questions(request):
	res = ''
	if request.method == 'GET':
		forum_url = request.GET['url']
		try:
			forum = Forum.objects.select_related().get(url=forum_url)
			questions = forum.questions.all()
			for question in questions:
				question.text = markdown(question.text)	
			res = get_date_formatted_json(questions)
			return HttpResponse(res, mimetype="application/javascript")
		except Exception, e:
			print "Error: could not process request for questions " + str(e)
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
			title = strip_tags(request.POST['title'])
			text = strip_tags(request.POST['question'])
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
		for answer in answers:
			answer.text = markdown(answer.text)
		res = get_date_formatted_json(answers)
		return HttpResponse(res, mimetype="application/javascript")
	except Exception, e:
		logging.error("Could not process request because: " + e)
		return HttpResponse("[{'error':'Could not process request'}]")


@user_passes_test(lambda u: u.is_authenticated(), "/accounts/login/")
def submit_answer(request, question_id):
	try:
		answer_text = strip_tags(request.POST['answer'])
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

			
def get_date_formatted_json(query_set):
	json_serializer = DateModifyingJSONSerializer() # serializers.get_serializer("json")()
	res = json_serializer.serialize(query_set)
	return res

