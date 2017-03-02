import datetime as dt
import time

from quiz.models import Quiz, QuizKey, DeployStatus
from roster.util import test_achiever

from util import *
from settings import *
from email import *

def deploy_url(key):
	return EXTERNAL_URL + '/quiz/%s/view/' % key

def deploy_keys(quiz, recepients):
	keys = []
	for a in recepients:
		if not QuizKey.objects.filter(quiz=quiz, achiever=a):
			qk = QuizKey(quiz=quiz,achiever=a)
			qk.key = random_quiz_key()
			qk.save()
			keys.append(qk)
	return keys

def deploy_quiz(quiz, testing_email=None, expire_days=120):
	is_test = testing_email != None
	quiz.deploy_status = DeployStatus.STARTED
	quiz.save()
	rec = [test_achiever()] if is_test else quiz.semester.achievers.all()
	quiz_keys = deploy_keys(quiz, rec)
	template = string.Template(quiz.email)
	for r in rec:
		qk = QuizKey.objects.get(quiz=quiz,achiever=r)
		text_rendered = template.substitute({
			'name': r.first_name,
			'title': quiz.title,
			'subtitle': quiz.subtitle,
			'url': deploy_url(qk.key),
			'expires': str(expire_days)
		})
		if not qk.email_success() or (is_test and qk.achiever == test_achiever()):
			req = fake_send_templated_email(
				recepient=testing_email or r.email,
				subject='New OTA and announcements from Amphibious Achievement!',
				body=text_rendered,
				p_success=1
			)
			qk.email_response = req.status_code
			qk.save()
	quiz.deploy_status = DeployStatus.UNDEPLOYED # Kludge alert
	if quiz.deploy_status == DeployStatus.STARTED:
		return
	quiz_keys = QuizKey.objects.filter(quiz=quiz)
	if not len([qk for qk in quiz_keys if not qk.email_success()]):
		if is_test:
			quiz.deploy_status = DeployStatus.SUCCESS_TEST
		else:
			quiz.deploy_status = DeployStatus.SUCCESS
	else:
		quiz.deploy_status = DeployStatus.PARTIAL
	quiz.save()
	


# Deprecated
def __deprecated_deploy_from_file(file,expire_days=365,delete_same_title=False,send_email=True,send_to_achievers=False,dry_run=False):
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
