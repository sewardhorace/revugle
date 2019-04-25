
from django.contrib import admin

from .models import Critic, Group, Review, Comment

admin.site.register(Critic)
admin.site.register(Group)
admin.site.register(Review)
admin.site.register(Comment)