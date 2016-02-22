import yaml
import json

from models import Quiz, Question, QUESTION_TYPES

def quiz_from_file(path):
	with open(path,'r') as file:
		return quiz_from_yaml('\n'.join(file.readlines()))

def quiz_from_yaml(str):
	d = yaml.load(str)
	assert d.get('title') and len(d['title']) > 0, "Quiz is missing title"
	assert d.get('subtitle') and len(d['subtitle']) > 0, "Quiz is missing subtitle"
	assert d.get('text') and len(d['text']) > 0, "Quiz is missing text body"
	assert d.get('questions') and len(d['questions']) > 0, "Quiz has no questions"
	questions = d['questions']
	for i, q in enumerate(questions):
		assert q.get('text'), "Question #%d has no text" % (i + 1)
		assert q.get('choices') and len(q['choices']) > 1, "Question #%d needs more than one choice" % (i + 1)
		assert q.get('correct'), "Question #%d is missing a correct answer" % (i + 1)
		assert q.get('correct') in q['choices'], "Question #%d has a correct answer that is not one of the choices" % (i + 1)
		if q.get('type'):
			assert q['type'] in [t[0] for t in QUESTION_TYPES]
	quiz = Quiz(
		title=d['title'],
		subtitle=d['subtitle'],
		text=d['text'],
	)
	quiz.save()
	for q in d['questions']:
		question = Question(
			text=q['text'],
			choices=json.dumps(q['choices']),
			correct=q['correct'],
			explanation=(q['explanation'] or '')
		)
		if q.get('type'):
			question.type = q['type']
		question.save()
		quiz.questions.add(question)
	return quiz



