from django.db import models
from achieve.roster.models import Achiever, Semester
from achieve.roster.util import current_semester

class DeployStatus(object):
	UNDEPLOYED = 0
	STARTED = 1
	PARTIAL = 2
	SUCCESS = 3
	SUCCESS_TEST = 4

QUESTION_TYPES = (
	('MC','Multiple Choice'),
	('SA','Select All'),
	('MI','Math Input'),
	('FB','Fill In The Blank'),
	('SA','Short Answer')
)

class Question(models.Model):
	type = models.CharField(max_length=2,choices=QUESTION_TYPES,default='MC')
	index = models.IntegerField()
	text = models.TextField()
	choices = models.TextField()
	correct = models.TextField()
	explanation = models.TextField(null=True,blank=True)

class Quiz(models.Model):
	title = models.CharField(max_length=100)
	subtitle = models.CharField(max_length=100)
	text = models.TextField()
	questions = models.ManyToManyField(Question)
	created = models.DateTimeField(auto_now=True)
	expires = models.DateTimeField(null=True,blank=True)
	email = models.TextField(default='')
	semester = models.ForeignKey(Semester,null=True)
	deploy_status = models.IntegerField(default=DeployStatus.UNDEPLOYED)

	def save(self, *args, **kwargs):
		if self.semester is None:  # Set default reference
			self.semester = current_semester()
		super(Quiz, self).save(*args, **kwargs)

class QuizKey(models.Model):
	quiz = models.ForeignKey(Quiz)
	achiever = models.ForeignKey(Achiever)
	key = models.CharField(max_length=10)
	accessed = models.DateTimeField(null=True,blank=True)
	email_response = models.IntegerField(default=0)

	def email_success(self):
		return self.email_response == 200

	def email_fail(self):
		return not self.email_success() and self.email_response > 0

	def email_started(self):
		return self.email_response > 0

class Response(models.Model):
	achiever = models.ForeignKey(Achiever)
	quiz = models.ForeignKey(Quiz)
	question = models.ForeignKey(Question)
	response = models.TextField()
	is_correct = models.BooleanField()
	time = models.DateTimeField(auto_now=True)

class Milestone(models.Model):
	achiever = models.ForeignKey(Achiever)
	response_count = models.IntegerField()
	time = models.DateTimeField(auto_now=True)
	claimed = models.BooleanField(default=False)
