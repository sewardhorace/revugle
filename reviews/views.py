
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
	return HttpResponse("Hello, world. You're at the reviews index.")

def login(request):
    template = loader.get_template('reviews/login.html')
    context = {}
    return render(request, 'reviews/login.html', context)

#@login_required(login_url='/')
def home(request):
    template = loader.get_template('reviews/home.html')
    context = {}
    return render(request, 'reviews/home.html', context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/home/')


'''
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

from django.shortcuts import get_object_or_404, render
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
'''