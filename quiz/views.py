import json
import datetime as dt

from django.http import HttpResponse
from models import *

def json_response(obj):
	return HttpResponse(json.dumps(obj),content_type='application/json')

def error_response(err):
	return json_response({'error':err})

def quiz_from_key(key):
	if QuizKey.objects.filter(key=key).exists():
		return QuizKey.objects.get(key=key)
	else:
		raise Exception

def view_quiz(request,key):
	try:
		qk = quiz_from_key(key)
	except:
		return error_response('invalid quiz key')
	r = HttpResponse('Okay')
	return r

def retrieve_quiz(request,key):
	try:
		qk = quiz_from_key(key)
	except:
		return error_response('invalid quiz key')
	quiz = qk.quiz
	achiever = qk.achiever
	responses = Response.objects.filter(achiever=achiever,quiz=quiz)
	res = {
		'achiever': achiever.full_name(),
		'id': quiz.id,
		'title': quiz.title,
		'subtitle': quiz.subtitle,
		'text': quiz.text,
		'questions': []
	}
	for qs in quiz.questions.all():
		qd = {
			'id': qs.id,
			'text': qs.text,
			'choices': json.loads(qs.choices),
		}
		if responses.filter(question=qs).exists():
			resp = responses.get(question=qs)
			qd['response'] = resp.response
			qd['correct'] = qd.correct
		res['questions'].append(qd)
	return json_response(res)

def accept_response(request,key):
	try:
		qk = quiz_from_key(key)
	except:
		return error_response('invalid quiz key')
	quiz = qk.quiz
	if dt.datetime.now() > quiz.expires:
		return error_response('quiz has expired')
	achiever = qk.achiever
	body = json.loads(request.body)
	if not body['question']:
		return error_response('no question specified')
	if not body['response']:
		return error_response('no response specified')
	if not Question.objects.exists(id=body['question']):
		return error_response('question does not exist')
	qs = Question.objects.get(id=body['question'])
	if Response.objects.get(achiever=qk.achiever,question=qs):
		return error_response('question has already been answered')
	resp = Response(
		quiz=quiz,
		achiever=achiever,
		question=qs,
		response=body['response'],
		is_correct=decide_if_correct(question,body['response'])
	)
	resp.save()
	return json_response({
		'res_id': resp.id,
		'question_id': qs.id,
		'correct': qs.correct,
		'explanation': qs.explanation,
		'is_correct': resp.is_correct
	})
	
	
