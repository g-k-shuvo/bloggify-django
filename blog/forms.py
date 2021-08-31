from django import forms
from django.db.models import fields
from django.forms.utils import ErrorList
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control','rows': '5'})
        }

class PostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].widget.attrs={'class': 'form-control'}
    class Meta:
        model = Post
        fields = ['topic', 'title', 'thumbnail', 'body']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }

class PostEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].widget.attrs={'class': 'form-control'}
    class Meta:
        model = Post
        fields = ['topic', 'title', 'thumbnail', 'body']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }