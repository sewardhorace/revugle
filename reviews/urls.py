from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('critic/<slug:critic_slug>/', views.critic, name='critic'),
    path('critic/<slug:critic_slug>/<slug:review_slug>/', views.review, name='review'),
    path('reviews/new/', views.create_review, name='create-review'),
    path('reviews/<int:review_id>/edit', views.update_review, name='update-review'),
    path('reviews/<int:review_id>/delete', views.delete_review, name='delete-review'),
    path('reviews/<int:review_id>/comment/', views.create_comment, name='create-comment'),
    path('logout/', views.logout, name='logout'),
]

#path('articles/<slug:title>/', views.article, name='article-detail'),