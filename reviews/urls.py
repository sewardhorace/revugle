from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('critics/<int:critic_id>/', views.critic, name='critic'),
    path('reviews/<int:review_id>/', views.review, name='review'),
    path('reviews/new/', views.review_form, name='review-form'),
    path('reviews/create/', views.create_review, name='create-review'),
    path('reviews/<int:review_id>/comment/', views.create_comment, name='create-comment'),
    path('logout/', views.logout, name='logout'),
]

#path('articles/<slug:title>/', views.article, name='article-detail'),