from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
]

#path('articles/<slug:title>/', views.article, name='article-detail'),