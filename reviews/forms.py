from django.forms import ModelForm
from .models import Review, Comment

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['subject', 'title', 'img_url', 'text', 'category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']