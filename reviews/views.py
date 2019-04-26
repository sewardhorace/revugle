
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Critic, Group, Review, Comment

#@login_required(login_url='/')
def home(request):
    reviews = Review.objects.order_by('-date')[:10]
    context = {'reviews': reviews}
    return render(request, 'reviews/home.html', context)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))


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