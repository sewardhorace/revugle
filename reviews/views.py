
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def index(request):
	return HttpResponse("Hello, world. You're at the reviews index.")

def login(request):
    template = loader.get_template('reviews/login.html')
    context = {}
    return HttpResponse(template.render(context, request))


#@login_required(login_url='/')
def home(request):
    template = loader.get_template('reviews/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/home/')