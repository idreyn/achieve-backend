from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
	url(r'^(?P<id>[A-Za-z0-9]+)/build/', build_quiz),
	url(r'^(?P<id>[A-Za-z0-9]+)/retrieve/', retrieve_quiz),
	url(r'^(?P<id>[A-Za-z0-9]+)/update/', update_quiz),
	url(r'^(?P<id>[A-Za-z0-9]+)/view/', view_quiz),
	url(r'^(?P<id>[A-Za-z0-9]+)/deploy/', deploy_quiz),
	url(r'^(?P<id>[A-Za-z0-9]+)/deploy-status/', deploy_status),
	url(r'^(?P<id>[A-Za-z0-9]+)/progress/', retrieve_progress),
)