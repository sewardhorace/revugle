
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import GroupForm, ReviewForm, CommentForm
from .models import Critic, Group, Review, Comment


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
        group=Group.objects.get(pk=request.POST['group']), 
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

def groups(request):
    groups = Group.objects.all()
    form = GroupForm()
    context = {'groups': groups, 'form': form}
    return render(request, 'reviews/groups.html', context)

def group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    reviews = Review.objects.filter(group=group_id).order_by('-date')[:10]
    context = {'group': group, 'reviews': reviews}
    return render(request, 'reviews/group.html', context)

@login_required
def create_group(request):
    critic = request.user.critic
    group = Group(
        name=request.POST['name'], 
        owner=critic)
    group.save()
    group.members.add(critic)
    return HttpResponseRedirect(reverse('group', args=(group.id,)))

@login_required
def manage_membership(request, group_id):

    critic = request.user.critic
    group = Group.objects.get(pk=group_id)

    if critic == group.owner:
        group.delete()
        return HttpResponseRedirect(reverse('groups'))
    elif critic in group.members.all():
        group.members.remove(critic)
    else:
        group.members.add(critic)

    return HttpResponseRedirect(reverse('group', args=(group_id,)))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))