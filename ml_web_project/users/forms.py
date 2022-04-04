from pyexpat import model
from attr import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    
    class Meta():
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=100, required=False)
    class Meta():
        model = User
        fields = ['first_name','last_name', 'username', 'email']