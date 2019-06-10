
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import ReviewForm, CommentForm
from .models import Critic, Review, Comment


def home(request):
    reviews = Review.objects.order_by('-date')[:10]
    context = {'reviews': reviews}
    return render(request, 'reviews/home.html', context)

def review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comments = Comment.objects.filter(target=review_id).order_by('-date')
    form = CommentForm()
    context = {'review': review, 'comments': comments, 'form': form}
    return render(request, 'reviews/review.html', context)

def review_form(request):
    form = ReviewForm()
    context = {'form': form}
    return render(request, 'reviews/review_form.html', context)

@login_required
def create_review(request):
    review = Review(
        author=request.user.critic, 
        subject=request.POST['subject'], 
        title=request.POST['title'],
        img_url=request.POST['img_url'],
        text=request.POST['text'],
        category=request.POST['category'])
    review.save()
    return HttpResponseRedirect(reverse('review', args=(review.id,)))

@login_required
def create_comment(request, review_id):
    comment = Comment(
        target=Review.objects.get(pk=review_id), 
        author=request.user.critic, 
        text=request.POST['text'])
    comment.save()
    return HttpResponseRedirect(reverse('review', args=(review_id,)))

def critic(request, critic_id):
    critic = get_object_or_404(Critic, pk=critic_id)
    reviews = Review.objects.filter(author=critic_id).order_by('-date')[:10]
    context = {'critic': critic, 'reviews': reviews}
    return render(request, 'reviews/critic.html', context)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))