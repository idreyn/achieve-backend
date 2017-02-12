import yaml
import markdown as md
import json
import re

from settings import EXTERNAL_URL
from models import Quiz, Question, QUESTION_TYPES

def parse_quiz_file(path):
	with open(path,'r') as file:
		return parse_quiz_yaml(path, '\n'.join(file.readlines()))


# Do some magic things
def make_sugar(path, quiz):
	# Replace bare image references (without http://) with imageroot
	def sugar(string):
		if quiz.get("imageroot"):
			string = re.sub(
				"!\[(.*)]\(((?!http://).*)\)",
				"![\\1](%s\\2)" % ("/" + quiz.get("imageroot") + "/"),
				str(string)
			)
		return string
	return sugar


def parse_quiz_yaml(path, string):
	d = yaml.load(string)
	sugar = make_sugar(path, d)
	assert d.get('title') and len(d['title']) > 0, "Quiz is missing title"
	assert d.get('subtitle') and len(d['subtitle']) > 0, "Quiz is missing subtitle"
	assert d.get('text') and len(d['text']) > 0, "Quiz is missing text body"
	assert d.get('questions') and len(d['questions']) > 0, "Quiz has no questions"
	assert d.get('email') and len(d['email']) > 0, "Quiz has no email message"
	email = d['email']
	for k in ['$name','$url']:
		assert k in email, "Quiz email is missing parameter %s" % k
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
		text=sugar(d['text']),
	)
	quiz.save()
	for i, q in enumerate(d['questions']):
		for choice in q['choices']:
			q['choices'][choice] = sugar(q['choices'][choice])
		question = Question(
			text=sugar(q['text']),
			choices=json.dumps(q['choices']),
			correct=q['correct'],
			explanation=sugar(q.get('explanation') or ''),
			index=i+1
		)
		if q.get('type'):
			question.type = q['type']
		question.save()
		quiz.questions.add(question)
	return md.markdown(email), quiz



