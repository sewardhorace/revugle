from itertools import chain
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from actstream import action
from actstream.actions import follow, unfollow
from actstream.models import actor_stream, user_stream

from .forms import ReviewForm, DeleteReviewForm, CommentForm, DeleteCommentForm
from .models import Critic, Review, Comment


def home(request):
    page = request.GET.get('page')
    if request.user.is_anonymous:
        reviews_list = Review.objects.order_by('-date')
        paginator = Paginator(reviews_list, 25)
        reviews = paginator.get_page(page)
        context = {'reviews': reviews}
        return render(request, 'reviews/home.html', context)
    else:
        action_stream = user_stream(request.user)
        paginator = Paginator(action_stream, 25)
        actions = paginator.get_page(page)
        context = {'actions': actions}
        return render(request, 'reviews/user_home.html', context)
    

def review(request, critic_slug, review_slug):
    critic = get_object_or_404(Critic, slug=critic_slug)
    review = get_object_or_404(Review, slug=review_slug, author=critic)
    comments = Comment.objects.filter(target=review.id).order_by('date')
    form = CommentForm()
    context = {'review': review, 'comments': comments, 'form': form}
    return render(request, 'reviews/review.html', context)

@login_required(login_url='/')
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user.critic
            review.save()
            action.send(request.user.critic, verb='posted', action_object=review)
            return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))
    else:
        form = ReviewForm()
        context = {'form': form}
    return render(request, 'reviews/create_review_form.html', context)

@login_required(login_url='/')
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
def upvote_review(request, review_id):
    user = request.user
    review = get_object_or_404(Review, pk=review_id)
    review.votes.delete(user.id)
    review.votes.up(user.id)
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def downvote_review(request, review_id):
    user = request.user
    review = get_object_or_404(Review, pk=review_id)
    review.votes.delete(user.id)
    review.votes.down(user.id)
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def delete_review_vote(request, review_id):
    user = request.user
    review = get_object_or_404(Review, pk=review_id)
    review.votes.delete(user.id)
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def create_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    comment = Comment(
        target=review, 
        author=request.user.critic, 
        text=request.POST['text'])
    comment.save()
    action.send(request.user.critic, verb='commented', action_object=comment, target=review)
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def delete_comment(request, comment_id):
    critic = request.user.critic
    comment = get_object_or_404(Comment, pk=comment_id)
    review = comment.target
    if not critic == comment.author:
        return HttpResponseForbidden();
    if request.method == 'POST':
        form = DeleteCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment.delete()
            return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))
    else:   
        return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def upvote_comment(request, comment_id):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.votes.delete(user.id)
    comment.votes.up(user.id)
    review = comment.target
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def downvote_comment(request, comment_id):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.votes.delete(user.id)
    comment.votes.down(user.id)
    review = comment.target
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

@login_required
def delete_comment_vote(request, comment_id):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.votes.delete(user.id)
    review = comment.target
    return HttpResponseRedirect(reverse('review', args=(review.author.slug, review.slug,)))

def critic(request, critic_slug):
    page = request.GET.get('page')
    critic = get_object_or_404(Critic, slug=critic_slug)
    action_stream = actor_stream(critic)
    paginator = Paginator(action_stream, 25)
    actions = paginator.get_page(page)
    context = {'critic': critic, 'actions':actions}
    return render(request, 'reviews/critic.html', context)

@login_required
def follow_critic(request, critic_id):
    user = request.user
    critic = get_object_or_404(Critic, pk=critic_id)
    follow(user, critic)
    return HttpResponseRedirect(reverse('critic', args=(critic.slug,)))

@login_required
def unfollow_critic(request, critic_id):
    user = request.user
    critic = get_object_or_404(Critic, pk=critic_id)
    unfollow(user, critic)
    return HttpResponseRedirect(reverse('critic', args=(critic.slug,)))

def search(request):
    page = request.GET.get('page')
    query_text = request.GET.get('query')

    #search critics
    search_vector = SearchVector('user__username', 'user__first_name', 'user__last_name', weight='A')
    search_query = SearchQuery(query_text)
    search_rank = SearchRank(search_vector, search_query)
    critics = Critic.objects.annotate(
        rank=search_rank
    ).filter(
        rank__gte=0.1
    )

    #search reviews
    search_vector = SearchVector('title', weight='A') + SearchVector('subject', weight='B') + SearchVector('text', weight='C')
    search_query = SearchQuery(query_text)
    search_rank = SearchRank(search_vector, search_query)
    reviews = Review.objects.annotate(
        rank=search_rank
    ).filter(
        rank__gte=0.1
    )

    #search comments
    search_vector = SearchVector('text', weight='A')
    search_query = SearchQuery(query_text)
    search_rank = SearchRank(search_vector, search_query)
    comments = Comment.objects.annotate(
        rank=search_rank
    ).filter(
        rank__gte=0.1
    )

    #combine results
    queryset_chain = chain(
        critics,
        reviews,
        comments
    )

    #sort by rank
    ranked_results = sorted(
        queryset_chain, 
        key=lambda instance: instance.rank, 
        reverse=True
    )

    #paginate
    paginator = Paginator(ranked_results, 25)
    results = paginator.get_page(page)

    context = {
        'query': query_text,
        'results': results
    }
    return render(request, 'reviews/search_results.html', context)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))