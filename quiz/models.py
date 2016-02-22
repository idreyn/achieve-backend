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

class QuizKey(models.Model):
	quiz = models.ForeignKey(Quiz)
	achiever = models.ForeignKey(Achiever)
	key = models.CharField(max_length=10)

class Response(models.Model):
	achiever = models.ForeignKey(Achiever)
	quiz = models.ForeignKey(Quiz)
	question = models.ForeignKey(Question)
	response = models.TextField()
	is_correct = models.BooleanField()