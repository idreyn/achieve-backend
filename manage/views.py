import json
from django.shortcuts import render

from ..util import json_response, error_response
from quiz.models import Quiz

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
		'questions': []
	}
	for qs in quiz.questions.order_by('id').all():
		res['questions'].append({
			'id': qs.id,
			'text': qs.text,
			'choices': json.loads(qs.choices),
			'correct': qs.correct,
			'explanation': qs.explanation,
		})
	return json_response(res)

