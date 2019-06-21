from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import pluralize
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from actstream import registry
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from vote.models import VoteModel

class Critic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.user.get_full_name()

class Review(VoteModel, models.Model):
    author = models.ForeignKey(Critic, on_delete=models.CASCADE)
    subject = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    text = MarkdownxField()
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
    GAMES = 'GAME'
    OTHER = 'OTHE'
    CATEGORY_CHOICES = (
        (HELPTEXT, '--Category--'),
        (BOOKS, 'Books'),
        (EVENTS, 'Events'),
        (GAMES, 'Games'),
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

    @property
    def score_display_text(self):
        text = '{} thumb{} {}'
        if self.vote_score < 0:
            count = self.vote_score * -1
            direction = 'down'
        else:
            count = self.vote_score
            direction = 'up'
        return text.format(count, pluralize(count), direction)

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

class Comment(VoteModel, models.Model):
    target = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(Critic, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    @property
    def score_display_text(self):
        text = '{} thumb{} {}'
        if self.vote_score < 0:
            count = self.vote_score * -1
            direction = 'down'
        else:
            count = self.vote_score
            direction = 'up'
        return text.format(count, pluralize(count), direction)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        if len(self.text) >= 100:
            return self.text[:97] + "..."
        else:
            return self.text