import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Forum(models.Model):
	url = models.CharField(max_length=255, primary_key=True)

	def __unicode__(self):
		return u"%s" % (self.url)

class Question(models.Model):
	time_asked = models.DateTimeField(blank=False, default=datetime.datetime.utcnow)
	title = models.CharField(max_length=255, blank=False)
	text = models.TextField()
	forum = models.ForeignKey(Forum, related_name='questions', blank=False)
	user = models.ForeignKey(User, blank=False, to_field='username')

	def __unicode__(self):
		return u"forum [%s] question [%s] user [%s]" % (self.forum, smart_truncate(self.text), self.user)

class Answer(models.Model):
	time_answered = models.DateTimeField(blank=False, default=datetime.datetime.utcnow)
	text = models.TextField(blank=False)
	question = models.ForeignKey(Question, related_name='answers', blank=False)
	user = models.ForeignKey(User, blank=False, to_field='username')

	def __unicode__(self):
		return u"question [%s] answer [%s] user [%s]" % (smart_truncate(question), smart_truncate(text), self.user)


def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

