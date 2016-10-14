import unicodecsv
import time

from roster.models import *
from models import *
from parse import *
from grader import *
from deploy import *
from util import *

def roster_from_csv(path,delimiter=',',yes_delete_current_roster=False):
	if not yes_delete_current_roster:
		print 'Please pass yes_delete_current_roster'
		return
	else:
		print 'Deleting current roster!'
		time.sleep(1)
		print 'You have five seconds to cancel (ctrl+c)...'
		time.sleep(5)
	print 'Loading roster from CSV file...'
	Achiever.objects.exclude(id=TEST_ACHIEVER.id).delete()
	with open(path,'rU') as file:
		cf = unicodecsv.reader(file,delimiter=delimiter,quotechar='|',encoding='ISO-8859-1')
		for row in cf:
			a = Achiever(
				first_name=row[0].strip(),
				last_name=row[1].strip(),
				email=row[2].strip().lower()
			)
			a.save()
			print '- %s => %s' % (a.full_name(),a.email)

def fix_keys(path,quiz_id,delimiter=','):
	print 'You fucked up! Fixing keys...'
	qz = Quiz.objects.get(id=quiz_id)
	with open(path,'rU') as file:
		cf = unicodecsv.reader(file,delimiter=delimiter,quotechar='|')
		for row in cf:
			first_name, last_name = map(lambda s: s.strip(),row[0].split(' '))
			key = row[1].strip()
			a = Achiever.objects.get(first_name=first_name,last_name=last_name)
			qk = QuizKey(
				achiever=a,
				quiz=qz,
				key=key
			)
			qk.save()
			print '- %s => %s' % (a.full_name(),qk.key)

def list_roster():
	achievers = Achiever.objects.all()
	print 'Roster (%d total):' % achievers.count()
	for a in achievers:
		print '- %s => %s' % (a.full_name(),a.email)

def list_quizzes():
	quizzes = Quiz.objects.all()
	for q in quizzes:
		print '%d => %s: %s (%s)' % (q.id,q.title,q.subtitle,human_date(q.created))

def quiz_details(quiz=None,id=None):
	if not quiz and not id:
		return
	if not quiz:
		if not Quiz.objects.filter(id=id).exists():
			print 'No quiz with id %d' % id
			return
		q = Quiz.objects.get(id=id)
	else:
		q = quiz
	questions = Question.objects.filter(quiz=q)
	print '%d => %s: %s (%s)' % (q.id,q.title,q.subtitle,human_date(q.created))
	achievers = Achiever.objects.all()
	results = [grade_quiz(a,q,questions) for a in achievers]
	attempted = [g for g in results if g[0].count() > 0]
	attempted_avg = (float(
		sum([a[1] for a in attempted])
	) / len(attempted)) if len(attempted) > 0 else 0
	completed = [g for g in results if g[0].count() == questions.count()]
	completed_avg = (float(
		sum([c[1] for c in completed])
	) / len(completed)) if len(completed) > 0 else 0
	print '%d/%d attempted with average score %d%%' % (len(attempted),achievers.count(),round(100 * attempted_avg))
	print '%d/%d completed with average score %d%%' % (len(completed),achievers.count(),round(100 * completed_avg))
	print '---------------------------------------'
	for responses, score, achiever  in results:
		qk = QuizKey.objects.filter(quiz=q,achiever=achiever)[0]
		if not qk:
			continue
		print "(%s) => %s: accessed %s, completed %d/%d for %d%%:" % (
			qk.key,
			achiever.full_name(),
			human_date(qk.accessed) if qk.accessed else 'NEVER',
			responses.count(),
			questions.count(),
			round(100 * score)
		)
		for r in responses:
			print '\tQuestion #%d => %s at %s' % (
				r.question.index,
				correct_string(r.is_correct),
				human_date(r.time) if r.time else 'NEVER'
			)

def progress(only_success=False):
	quizzes = Quiz.objects.all()
	for a in Achiever.objects.all():
		pr = []
		for q in quizzes:
			qs = Question.objects.filter(quiz=q)
			resp, _, _ = grade_quiz(a,q,qs)
			pr.append(str(resp.count()))
		print '%s: %s' % (a.full_name(),''.join(pr))




