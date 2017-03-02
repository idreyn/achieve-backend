import json
import time
import string
import markdown as md

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from settings import *
from ..util import json_response, error_response
from quiz.models import Quiz, Question, QuizKey, DeployStatus
import quiz.deploy as deploy

def view_dashboard(request):
	return render(request, 'dashboard.html')

def build_quiz(request, id):
	return render(request, 'builder.html')

def view_quiz(request, id):
	return render(request, 'quiz.html')

# Get JSON representation of quiz
def retrieve_quiz(request, id):
	quiz = Quiz.objects.get(id=id)
	res = {
		'id': quiz.id,
		'title': quiz.title,
		'subtitle': quiz.subtitle,
		'text': quiz.text,
		'email': quiz.email,
		'questions': []
	}
	for qs in quiz.questions.order_by('index').all():
		res['questions'].append({
			'id': qs.id,
			'text': qs.text,
			'choices': json.loads(qs.choices),
			'correct': qs.correct,
			'explanation': qs.explanation,
		})
	return json_response(res)

# Basically a dummy route for symmetry with /quiz
def retrieve_progress(request, id):
	return json_response({
		'name': "Test Achiever",
		'quizzes': [],
		'milestones': {
			'complete': 0,
			'needed': 15,
			'unclaimed': []
		}
	})

def preview_email(request, id):
	quiz = Quiz.objects.get(id=id)
	template = string.Template(md.markdown(quiz.email))
	text_rendered = template.substitute({
		'name': 'Test Achiever',
		'title': quiz.title,
		'subtitle': quiz.subtitle,
		'url': '#',
		'expires': str(120)
	})
	return HttpResponse(render_to_string('email-template.html', {
		'STATIC_URL': EXTERNAL_URL + STATIC_URL,
		'title': 'New OTA and announcements from Amphibious Achievement!',
		'content': text_rendered
	}))

def update_quiz(request, id):
	data = json.loads(request.raw_post_data)
	quiz = Quiz.objects.get(id=id)
	quiz.title = data.get("title", quiz.title)
	quiz.subtitle = data.get("subtitle", quiz.subtitle)
	quiz.text = data.get("text", quiz.text)
	quiz.email = data.get("email", quiz.email)
	qids = []
	for qd in data.get("questions",[]):
		qid = qd.get("id", None)
		if not qid:
			q = Question(
				index=qd['index'],
				text=qd.get('text',''),
				choices=json.dumps(qd.get('choices',{})),
				explanation=qd.get('explanation'),
				correct=qd.get('correct','')
			)
			q.save()
			qids.append(q.id)
			quiz.questions.add(q)
		else:
			q = Question.objects.get(id=qid)
			q.text = qd.get('text','')
			q.choices = json.dumps(qd['choices'])
			q.correct = qd.get('correct','')
			q.explanation = qd.get('explanation')
			q.index = qd['index']
			qids.append(q.id)
			q.save()
	# Look for questions that don't exist and delete them
	for q in Question.objects.filter(quiz=quiz):
		if not q.id in qids:
			q.delete()
	quiz.save()
	return retrieve_quiz(request, id)

def deploy_status(request, id):
	quiz = Quiz.objects.get(id=id)
	quiz_keys = QuizKey.objects.filter(quiz=quiz)
	return json_response({
		"status": quiz.deploy_status,
		"email_success": len([qk for qk in quiz_keys if qk.email_success()]),
		"email_fail": len([qk for qk in quiz_keys if qk.email_fail()]),
		"email_pending": [
			qk.achiever.full_name() for qk in quiz_keys if not qk.email_success()
		],
		"email_total": len(quiz_keys)
	})

def deploy_quiz(request, id):
	try:
		data = json.loads(request.raw_post_data)
	except:
		data = {}
	quiz = Quiz.objects.get(id=id)
	if data.get("abandon"):
		quiz.deploy_status = DeployStatus.UNDEPLOYED
		quiz.save()
	else:
		quiz.deploy_status = DeployStatus.STARTED
		quiz.save()
		deploy.deploy_quiz(quiz, testing_email=data.get("email"))
	return deploy_status(request, id)

