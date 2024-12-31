# forms.py
from django import forms
from .models import Property 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'address','contact', 'image']
    image = forms.ImageField(required=False)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
