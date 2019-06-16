from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Critic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.user.get_full_name()

class Review(models.Model):
    author = models.ForeignKey(Critic, on_delete=models.CASCADE)
    subject = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    text = MarkdownxField()
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    private = models.BooleanField(default=False)

    HELPTEXT = ''
    MOVIES = 'MOVI'
    TV = 'TV'
    MUSIC = 'MUSI'
    BOOKS = 'BOOK'
    EVENTS = 'EVEN'
    PLACES = 'PLAC'
    PRODUCTS = 'PROD'
    OTHER = 'OTHE'
    CATEGORY_CHOICES = (
        (HELPTEXT, '--Category--'),
        (BOOKS, 'Books'),
        (EVENTS, 'Events'),
        (MOVIES, 'Movies'),
        (MUSIC, 'Music'),
        (PLACES, 'Places'),
        (PRODUCTS, 'Products'),
        (TV, 'TV'),
        (OTHER, 'Other'),
    )
    category = models.CharField(
        max_length=4,
        choices=CATEGORY_CHOICES,
        default=HELPTEXT,
    )

    @property
    def formatted_text(self):
        return mark_safe(markdownify(self.text))

    class Meta:
        ordering = ('date',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'], name='unique_title')
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs) 

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