import json
from django.shortcuts import render

from ..util import json_response, error_response
from quiz.models import Quiz, Question

def build_quiz(request, id):
	return render(request, 'builder.html')

# Get JSON representation of quiz
def retrieve_quiz(request, id):
	quiz = Quiz.objects.get(id=id)
	res = {
		'id': quiz.id,
		'title': quiz.title,
		'subtitle': quiz.subtitle,
		'text': quiz.text,
		'deployed': quiz.deployed,
		'deployed_successfully': quiz.deployed_successfully(),
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

def update_quiz(request, id):
	data = json.loads(request.raw_post_data)
	quiz = Quiz.objects.get(id=id)
	quiz.title = data.get("title", quiz.title)
	quiz.subtitle = data.get("subtitle", quiz.subtitle)
	quiz.text = data.get("text", quiz.text)
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



def view_quiz(request, id):
	return render(request, 'quiz.html')

