from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Course(models.Model):
	short_name = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=100, blank=False)
	description = models.CharField(max_length=2048, blank=False)

	def __unicode__(self):
		return u"[%s] %s" % (self.short_name, self.name)

class Topic(models.Model):
	title = models.CharField(max_length=128)
	content = models.TextField(blank=False)
	course = models.ForeignKey(Course, blank=False)

	def __unicode__(self):
		return u"%s" % (self.title)

class CourseOrder(models.Model):	
	course = models.ForeignKey(Course, blank=False)
	order = models.IntegerField(blank=False)
	
class TopicOrder(models.Model):	
	course = models.ForeignKey(Course, blank=False)
	topic = models.ForeignKey(Topic, blank=False)
	order = models.IntegerField(blank=False)
	
	def __unicode__(self):
		return u"Course[%s] Topic[%s] Order - %d" % (self.course, self.topic, self.order)

class Forum(models.Model):
	url = models.CharField(max_length=255, primary_key=True)

	def __unicode__(self):
		return u"%s" % (self.url)

class Question(models.Model):
	title = models.CharField(max_length=255, blank=False)
	text = models.TextField()
	forum = models.ForeignKey(Forum, related_name='questions', blank=False)
	user = models.ForeignKey(User, blank=False, to_field='username')

	def __unicode__(self):
		return u"forum [%s] question [%s] user [%s]" % (self.forum, smart_truncate(self.text), self.user)

class Answer(models.Model):
	text = models.TextField(blank=False)
	question = models.ForeignKey(Question, related_name='answers', blank=False)
	user = models.ForeignKey(User, blank=False, to_field='username')

	def __unicode__(self):
		return u"question [%s] answer [%s] user [%s]" % (smart_truncate(question), smart_truncate(text), self.user)


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True, related_name='profile', blank=False)
	full_name = models.CharField(max_length=255, blank=False)
	email = models.EmailField(blank=False)
	website = models.CharField(max_length=255, blank=True)
	timezone = models.CharField(max_length="20", blank=True)
	bio = models.TextField(blank=True)
	
	def __unicode__(self):
		return u"Name [%s]" % (self.full_name)


def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

#signal handling
#todo Refactor this if we find a better place to put this code
def post_user_saved(sender, **kwargs):
	user_profile = UserProfile.objects.get_or_create(user=kwargs['instance'])

post_save.connect(post_user_saved, sender=User)
