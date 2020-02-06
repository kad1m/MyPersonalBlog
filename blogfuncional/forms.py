from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'image', 'category', 'text', 'article_description',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

