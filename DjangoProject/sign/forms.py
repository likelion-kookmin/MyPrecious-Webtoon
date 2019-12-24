from django import froms
from django.contrib.auth.models import Users

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'em', 'ps']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        # 로그인 시에 유저id와 비밀번호만
        fields = ['id', 'ps']

