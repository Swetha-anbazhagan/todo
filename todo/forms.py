from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TODO

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TODOForm(forms.ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'description', 'completed']
