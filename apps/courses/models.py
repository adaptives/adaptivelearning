import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Course(models.Model):
	short_name = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=100, blank=False)
	description = models.TextField(blank=False)

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


class UserProfile(models.Model):
	TIMEZONE_CHOICES = (
		('UTC -12', 'UTC -12'),
		('UTC -11', 'UTC -11'),
		('UTC -10', 'UTC -10'),
		('UTC -9:30', 'UTC -9:30'),
		('UTC -9', 'UTC -9'),
		('UTC -8', 'UTC -8'),
		('UTC -7', 'UTC -7'),
		('UTC -6', 'UTC -6'),
		('UTC -5', 'UTC -5'),
		('UTC -4:30', 'UTC -4:30'),
		('UTC -4', 'UTC -4'),
		('UTC -3:30', 'UTC -3:30'),
		('UTC -2', 'UTC -2'),
		('UTC -1', 'UTC -1'),
		('UTC', 'UTC'),
		('UTC +1', 'UTC +1'),
		('UTC +2', 'UTC +2'),
		('UTC +3', 'UTC +3'),
		('UTC +3:30', 'UTC +3:30'),
		('UTC +4', 'UTC +4'),
		('UTC +4:30', 'UTC +4:30'),
		('UTC +5', 'UTC +5'),
		('UTC +5:30', 'UTC +5:30'),
		('UTC +5:45', 'UTC +5:45'),
		('UTC +6', 'UTC +6'),
		('UTC +6:30', 'UTC +6:30'),
		('UTC +7', 'UTC +7'),
		('UTC +8', 'UTC +8'),
		('UTC +8:45', 'UTC +8:45'),
		('UTC +9', 'UTC +9'),
		('UTC +10', 'UTC +10'),
		('UTC +10:30', 'UTC +10:30'),
		('UTC +11', 'UTC +11'),
		('UTC +11:30', 'UTC +11:30'),
		('UTC +12', 'UTC +12'),
		('UTC +12:45', 'UTC +12:45'),
		('UTC +13', 'UTC +13'),
		('UTC +14', 'UTC +14'),
	)
	user = models.ForeignKey(User, unique=True, related_name='profile', blank=False)
	full_name = models.CharField(max_length=255, blank=False)
	email = models.EmailField(blank=False)
	website = models.CharField(max_length=255, blank=True)
	timezone = models.CharField(max_length="20", blank=True, choices=TIMEZONE_CHOICES)
	bio = models.TextField(blank=True)
	
	def __unicode__(self):
		return u"Name [%s]" % (self.full_name)


#signal handling
#todo Refactor this if we find a better place to put this code
def post_user_saved(sender, **kwargs):
	user_profile = UserProfile.objects.get_or_create(user=kwargs['instance'])

post_save.connect(post_user_saved, sender=User)
