import datetime as dt
import time

from models import *
from parse import *
from util import *
from settings import *
from email import *

TEST_ACHIEVER = Achiever.objects.get(first_name='Test',last_name='Achiever')

def deploy_from_file(file,expire_days=365,delete_same_title=False,send_email=True,send_to_achievers=False,dry_run=False):
	email, quiz = parse_quiz_file(file)
	expire_date = dt.datetime.now() + dt.timedelta(days=expire_days)
	quiz.expires = expire_date
	quiz.source_file = file
	quiz.save()
	print 'Created quiz "%s" with %d questions, expiring on %s!' % (quiz.title,quiz.questions.count(),human_date(expire_date))
	if not quiz:
		print 'Something has gone terribly wrong'
		return None
	same = Quiz.objects.exclude(pk=quiz.pk).filter(title=quiz.title)
	if same.count() > 0:
		if delete_same_title:
			print 'Deleting quizzes with same name and all of their related entries...'
			for s in same:
				print '- %s of %s' % (s.title,human_date(s.created))
				for q in s.questions.all():
					q.delete()
				Response.objects.filter(quiz=s).delete()
				QuizKey.objects.filter(quiz=s).delete()
				s.delete()
		else:
			print 'Refusing to deploy a quiz with duplicate name. Deleting...'
			for q in quiz.questions.all():
				q.delete()
			quiz.delete()
			return
	deploy_keys(quiz)
	if send_email:
		deploy_emails(email,quiz,expire_days,send_to_achievers,dry_run)

def deploy_keys(quiz):
	QuizKey.objects.filter(quiz=quiz).delete()
	print 'Creating keys...'
	for a in Achiever.objects.all():
		qk = QuizKey(quiz=quiz,achiever=a)
		qk.key = random_quiz_key()
		print '- %s => %s' % (a.full_name(),qk.key)
		qk.save()

def deploy_emails(text,quiz,expire_days,send_to_achievers=False,dry_run=False):
	print 'Deploying emails...'
	if dry_run:
		print '(Dry run)'
	if send_to_achievers:
		print '(Sending to achievers)'
		time.sleep(5)
	if send_to_achievers:
		rec = Achiever.objects.all()
	else:
		rec = Achiever.objects.filter(id=TEST_ACHIEVER.id)
	template = string.Template(text)
	for r in rec:
		qk = QuizKey.objects.get(quiz=quiz,achiever=r)
		text_rendered = template.substitute({
			'name': r.first_name,
			'title': quiz.title,
			'subtitle': quiz.subtitle,
			'url': deploy_url(qk.key),
			'expires': str(expire_days)
		})
		if dry_run:
			print '- %s => %d' % (r.full_name(), 0)
		else:
			req = send_templated_email(
				recepient=r.email,
				subject='New OTA and announcements from Amphibious Achievement!',
				body=text_rendered
			)
			print '- %s => %d' % (r.full_name(), req.status_code)
	if not dry_run and send_to_achievers:
		quiz.deployed = True
		quiz.save()

def deploy_url(key):
	return EXTERNAL_URL + '/quiz/%s/view/' % key


