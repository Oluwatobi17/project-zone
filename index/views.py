from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return HttpResponse("<h1>Ganiu Ibrahim: This website is under maintanance<br/>Please check back for Ganiu Ibrahim's project</h1>")