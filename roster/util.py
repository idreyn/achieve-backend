import datetime
from roster.models import *

def current_semester():
	now = datetime.datetime.now()
	is_spring = now.month <= 6 # Kinda arbitrarily roll over in July
	return Semester.objects.get_or_create(year=now.year, is_spring=is_spring)[0]

def test_achiever():
	return Achiever.objects.get_or_create(
		first_name='Test',
		last_name='Achiever',
		email='idreyn@gmail.com'
	)[0]