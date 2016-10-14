from models import *

def decide_if_correct(question, response):
	return question.correct == response

def correct_string(b):
	return 'correct' if b else 'incorrect'

def grade_quiz(achiever, quiz, questions=None):
	if questions is None:
		questions = quiz.questions
	responses = Response.objects.filter(achiever=achiever, quiz=quiz)
	score = float(responses.filter(is_correct=True).count()) / questions.count()
	return (responses, score, achiever)