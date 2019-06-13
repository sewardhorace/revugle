
from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import Critic, Review, Comment

admin.site.register(Critic)
admin.site.register(Review, MarkdownxModelAdmin)
admin.site.register(Comment)