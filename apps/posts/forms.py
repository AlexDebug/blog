from .models import Post, Comment
from django.forms import ModelForm, Textarea


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
        ]
        widgets = {'content': Textarea(attrs={'cols': 80, 'rows': 20}),}


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'title',
            'content',
        ]
        widgets = {'content': Textarea(attrs={'cols': 80, 'rows': 20}), }

