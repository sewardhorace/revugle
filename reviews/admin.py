
from django.contrib import admin

from .models import Critic, Review, Comment

admin.site.register(Critic)
admin.site.register(Review)
admin.site.register(Comment)