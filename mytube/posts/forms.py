from django import forms
from .models import Post, Comment
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['text', 'group', 'images']

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    images = forms.ImageField(required=False)


class CommentFrom(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
