import string
import random

from roster.models import *
from models import *
from parse import *
import datetime as dt

def random_quiz_key(length=10):
	bank = list(string.ascii_letters + string.digits)
	while True:
		generate = ''.join(
			[random.choice(bank) for i in xrange(length)]
		)
		if not QuizKey.objects.filter(key=generate).exists():
			return generate

def deploy_from_file(file,expire_days=7,delete_same_name=True,send_to_test=False,send_to_achievers=False):
	quiz = quiz_from_file(file)
	expire_date = dt.datetime.now() + dt.timedelta(days=expire_days)
	quiz.expires = expire_date
	print 'Created quiz %s with %d questions, expiring on %s...' % (quiz.title,quiz.questions.count(),str(expire_date))
	if not quiz:
		return None
	if delete_same_name:
		same = Quiz.objects.exclude(pk=quiz.pk).filter(title=quiz.title)
		for s in same:
			print 'Deleting %s of %s and all of its related entries...' % (s.title,str(s.created))
			for q in s.questions.all():
				q.delete()
			Response.objects.filter(quiz=s).delete()
			QuizKey.objects.filter(quiz=s).delete()
			s.delete()
	quiz.save()
	deploy_keys(quiz)

def deploy_keys(quiz):
	QuizKey.objects.filter(quiz=quiz).delete()
	for a in Achiever.objects.all():
		qk = QuizKey(quiz=quiz,achiever=a)
		qk.key = random_quiz_key()
		print 'Creating key for %s => %s ... %s' % (quiz.title,a.full_name(),qk.key)
		qk.save()
