from django.db import models
from django.contrib.auth.models import User

class Critic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class Review(models.Model):
    author = models.ForeignKey(Critic, on_delete=models.CASCADE)
    subject = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    img_url = models.URLField(blank=True)
    text = models.TextField()
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)
    private = models.BooleanField(default=False)

    MOVIES = 'MOVI'
    TV = 'TV'
    MUSIC = 'MUSI'
    BOOKS = 'BOOK'
    EVENTS = 'EVEN'
    PLACES = 'PLAC'
    PRODUCTS = 'PROD'
    OTHER = 'OTHE'
    CATEGORY_CHOICES = (
        (MOVIES, 'Movies'),
        (TV, 'TV'),
        (MUSIC, 'Music'),
        (BOOKS, 'Books'),
        (EVENTS, 'Events'),
        (PLACES, 'Places'),
        (PRODUCTS, 'Products'),
        (OTHER, 'Other'),
    )
    category = models.CharField(
        max_length=4,
        choices=CATEGORY_CHOICES,
        default=OTHER,
    )

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    target = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(Critic, on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.text