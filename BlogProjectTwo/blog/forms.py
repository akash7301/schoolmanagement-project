from django import forms
from blog.models import *
from django.contrib.auth.models import User

class EmailSendForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','slug','auther','body','status','tags']
        prepopulated_fields = {'slug':('title',)}
