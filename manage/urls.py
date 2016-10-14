from django.conf.urls.defaults import patterns, include, url

from views import build_quiz, retrieve_quiz

urlpatterns = patterns('',
	url(r'^(?P<id>[A-Za-z0-9]+)/build/', build_quiz),
	url(r'^(?P<id>[A-Za-z0-9]+)/retrieve/', retrieve_quiz),
)