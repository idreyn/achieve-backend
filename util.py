import json
from django.http import HttpResponse

def json_response(obj):
	return HttpResponse(json.dumps(obj),content_type='application/json')

def error_response(err):
	return json_response({'error':err})