import random
import string

from models import QuizKey
from roster.models import *

def human_date(d):
	return d.strftime("%Y-%m-%d @ %H:%M")

def random_quiz_key(length=10):
	bank = list(string.ascii_letters + string.digits)
	while True:
		generate = ''.join(
			[random.choice(bank) for i in xrange(length)]
		)
		if not QuizKey.objects.filter(key=generate).exists():
			return generate

