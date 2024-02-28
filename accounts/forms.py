from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label='Email / Username')
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()
