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

	

