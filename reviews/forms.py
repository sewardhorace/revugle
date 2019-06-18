from django.forms import ModelForm, TextInput, Textarea
from django.utils.translation import gettext_lazy as _
from .models import Review, Comment

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'subject', 'category', 'text')
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title'}),
            'subject': TextInput(attrs={'placeholder': 'Subject'}),
        }

class DeleteReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'placeholder': 'Leave a comment...'})
        }

class DeleteCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ()