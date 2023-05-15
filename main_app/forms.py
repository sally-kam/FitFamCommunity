from django.forms import ModelForm, Textarea
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput


    

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    date_of_birth = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d', attrs={'style': 'width: 200px;'}), required=True)
    bio = forms.CharField(max_length=5000, widget=Textarea(attrs={'rows': 8, 'cols': 80}))
    
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]
        

    


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': Textarea(attrs={'rows': 2, 'cols': 80}),
            'content': Textarea(attrs={'rows': 10, 'cols': 80}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'rows': 10, 'cols': 80})
        }
        labels = {
            'text': 'Comment'
        }


class EditProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(label='Profile Picture')
    date_of_birth = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d', attrs={'style': 'width: 200px;'}), label='Date of Birth')
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 9}),
        max_length=1000,
        required=False,
    )

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'bio', 'profile_pic']

        