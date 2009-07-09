from django.db import models

class Course(models.Model):
	short_name = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=2048)

	def __unicode__(self):
		return u"[%s] %s" % (self.short_name, self.name)

class Topic(models.Model):
	title = models.CharField(max_length=128)
	content = models.TextField()
	course = models.ManyToManyField(Course)

	def __unicode__(self):
		return u"%s" % (self.title)

class CourseOrder(models.Model):	
	course = models.ForeignKey(Course)
	order = models.IntegerField()
	
class TopicOrder(models.Model):	
	course = models.ForeignKey(Course)
	topic = models.ForeignKey(Topic)
	order = models.IntegerField()
	
	def __unicode__(self):
		return u"Course[%s] Topic[%s] Order - %d" % (self.course, self.topic, self.order)

class Forum(models.Model):
	url = models.CharField(max_length=256, primary_key=True)

	def __unicode__(self):
		return u"%s" % (self.url)

class Question(models.Model):
	text = models.TextField()
	forum = models.ForeignKey(Forum)

	def __unicode__(self):
		return u"forum [%s] %s" % (self.forum, smart_truncate(self.text))

class Answer():
	text = models.TextField()
	question = models.ForeignKey(Question)

	def __unicode__(self):
		return u"question [%s] answer [%s] " % (smart_truncate(question), smart_truncate(text))

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
