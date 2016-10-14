from django.template.loader import render_to_string

from models import *
from email import *

MILESTONE = 15

def handle_milestone(achiever, count=None):
	if count is None:
		count = Response.objects.filter(achiever=achiever).count()
	last_milestone = 0
	ms = Milestone.objects.filter(achiever=achiever)
	if ms.count() > 0:
		last_milestone = max([m.response_count for m in ms])
	if count - last_milestone >= MILESTONE:
		m = Milestone(achiever=achiever, response_count=last_milestone + MILESTONE)
		m.save()
		return [m] + handle_milestone(achiever, count) # In case we hit multiple
	return []

def get_milestone(achiever):
	count = Response.objects.filter(achiever=achiever).count()
	return (count % MILESTONE, MILESTONE)

def claim_next_milestone(achiever):
	ms = Milestone.objects.filter(achiever=achiever,claimed=False)
	if ms.count():
		milestone = ms[0]
		body =  """
			Hi %s,
			<p>You've earned a reward for your hard work with the OTAs 
			&mdash; a trip to Tosci's (or equivalent snackage) with a mentor or fellow Achiever! 
			Show this email to your mentor to get the ball rolling!</p>
			<p>Best,
			<br>
			Team Academics</p>
		""" % (achiever.first_name)
		req = send_templated_email(
			recepient=achiever.email,
			subject="Your OTA reward!",
			body=body
		)
		if req.status_code == 200:
			milestone.claimed = True
			milestone.save()
			return True
		else:
			return False
	else:
		return False