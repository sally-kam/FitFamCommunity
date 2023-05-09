from django.forms import ModelForm, Textarea
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput


    

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    date_of_birth = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'date_of_birth')
    

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': Textarea(attrs={'rows': 2, 'cols': 80}),
            'content': Textarea(attrs={'rows': 10, 'cols': 80}),
        }
