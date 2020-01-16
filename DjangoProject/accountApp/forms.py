from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from allauth.account.forms import LoginForm, SignupForm

User = get_user_model()


class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'type':'email', 'class': 'input is-info', 'style':'width:1000px;margin-bottom:10px;'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={'type':'password', 'class': 'input is-info', 'style':'width:1000px;margin-bottom:10px;'})

        self.fields['login'].label = "e-mail"
        self.fields['password'].label = "password"

class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={
            'type':'email', 'class': 'input is-info', 'style':'width:1000px;margin-bottom:10px;'
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={'type':'password1', 'class': 'input is-info', 'style':'width:1000px;margin-bottom:10px;'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'type':'password2', 'class': 'input is-info', 'style':'width:1000px;margin-bottom:10px;'})
        self.fields['email'].label = "e-mail"
        self.fields['password1'].label = "password"
        self.fields['password2'].label = "confirm password"
    

