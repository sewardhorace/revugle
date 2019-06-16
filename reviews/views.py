
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import ReviewForm, DeleteReviewForm, CommentForm
from .models import Critic, Review, Comment


def home(request):
    reviews = Review.objects.order_by('-date')[:10]
    context = {'reviews': reviews}
    return render(request, 'reviews/home.html', context)

def review(request, critic_slug, review_slug):
    critic = get_object_or_404(Critic, slug=critic_slug)
    review = get_object_or_404(Review, slug=review_slug, author=critic)
    comments = Comment.objects.filter(target=review.id).order_by('-date')
    form = CommentForm()
    context = {'review': review, 'comments': comments, 'form': form}
    return render(request, 'reviews/review.html', context)

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user.critic
            review.save()
            return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))
    else:
        form = ReviewForm()
        context = {'form': form}
    return render(request, 'reviews/create_review_form.html', context)

@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if not request.user.critic == review.author:
        return HttpResponseForbidden();
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))
    else:   
        form = ReviewForm(instance=review)
        context = {'form': form, 'review':review}
    return render(request, 'reviews/update_review_form.html', context)

@login_required
def delete_review(request, review_id):
    critic = request.user.critic
    review = get_object_or_404(Review, pk=review_id)
    if not critic == review.author:
        return HttpResponseForbidden();
    if request.method == 'POST':
        form = DeleteReviewForm(request.POST, instance=review)
        if form.is_valid():
            review.delete()
            return HttpResponseRedirect(reverse('critic', args=(critic.slug,)))
    else:   
        return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def create_comment(request, review_id):
    review = Review.objects.get(pk=review_id)
    comment = Comment(
        target=review, 
        author=request.user.critic, 
        text=request.POST['text'])
    comment.save()
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

def critic(request, critic_slug):
    critic = get_object_or_404(Critic, slug=critic_slug)
    reviews = Review.objects.filter(author=critic.id).order_by('-date')[:10]
    context = {'critic': critic, 'reviews': reviews}
    return render(request, 'reviews/critic.html', context)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))