from django.forms import ModelForm
from .models import Group, Review, Comment

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['group', 'subject', 'title', 'img_url', 'text', 'category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']