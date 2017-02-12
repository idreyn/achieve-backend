from django.db import models

from achieve.roster.models import Achiever

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
	deployed = models.BooleanField(default=False)

	def deployed_successfully(self):
		return QuizKey.objects.filter(quiz=self, mail_success=False).count() == 0

class QuizKey(models.Model):
	quiz = models.ForeignKey(Quiz)
	achiever = models.ForeignKey(Achiever)
	key = models.CharField(max_length=10)
	accessed = models.DateTimeField(null=True,blank=True)
	mail_success = models.BooleanField(default=False)

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
