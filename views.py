from django.http import HttpResponse
from django.shortcuts import render_to_response

def manage(request):
	return render_to_response('manage.html')
