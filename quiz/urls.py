from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
	url(r'^(?P<key>[A-Za-z0-9]+)/view/',view_quiz),
	url(r'^(?P<key>[A-Za-z0-9]+)/retrieve/',retrieve_quiz),
	url(r'^(?P<key>[A-Za-z0-9]+)/respond/',accept_response)
)