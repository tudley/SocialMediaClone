from django import forms
from .models import Post, Comment, Picture

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text' : ''}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text' : ''}

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['file', 'caption']
        labels = {'file' : '', 'caption' : ''}
