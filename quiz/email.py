import requests

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