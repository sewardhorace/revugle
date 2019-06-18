from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('critic/<slug:critic_slug>/', views.critic, name='critic'),
    path('critic/<slug:critic_slug>/<slug:review_slug>/', views.review, name='review'),
    path('reviews/new/', views.create_review, name='create-review'),
    path('reviews/<int:review_id>/edit', views.update_review, name='update-review'),
    path('reviews/<int:review_id>/delete', views.delete_review, name='delete-review'),
    path('reviews/<int:review_id>/upvote/', views.upvote_review, name='upvote-review'),
    path('reviews/<int:review_id>/downvote/', views.downvote_review, name='downvote-review'),
    path('reviews/<int:review_id>/delete-vote/', views.delete_review_vote, name='delete-review-vote'),
    path('reviews/<int:review_id>/comment/', views.create_comment, name='create-comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
    path('comments/<int:comment_id>/upvote/', views.upvote_comment, name='upvote-comment'),
    path('comments/<int:comment_id>/downvote/', views.downvote_comment, name='downvote-comment'),
    path('comments/<int:comment_id>/delete-vote/', views.delete_comment_vote, name='delete-comment-vote'),
    path('logout/', views.logout, name='logout'),
]