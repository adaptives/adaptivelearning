import logging
import datetime
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import Serializer as JSONSerializer 
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from courses.models import Forum
from courses.models import Question
from courses.models import Answer

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

