import requests
import time
from random import random
from django.template.loader import render_to_string

from settings import *

def send_email(recepient, subject, body):
	return requests.post(
		MAILGUN_REQUEST_URL,
		auth=('api',MAILGUN_API_KEY),
		data={
			'from': 'amphibious-academics@amphibious-ota.mit.edu',
			'to': recepient,
			'subject': subject,
			'html': body,
		}
	)

def send_templated_email(recepient, subject, body):
	body = render_to_string('email-template.html',{
		'STATIC_URL': EXTERNAL_URL + STATIC_URL,
		'title': subject,
		'content': body
	})
	return send_email(recepient, subject, body)

class FakeResponse(object):
	def __init__(self, status_code):
		self.status_code = status_code

def fake_send_templated_email(recepient, subject, body, p_success):
	time.sleep(0.5)
	return FakeResponse(200 if random() < p_success else 400)

