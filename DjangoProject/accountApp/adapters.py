from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(CustomAccountAdapter, self).save_user(request, user, form, commit)
        user.profile = Profile.objects.create(user=user)
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    # social 로그인 시 생성되는 user
    def save_user(self, request, sociallogin, form=None):
        user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form)
        user.profile = Profile.objects.create(user=user)

        extra_data = sociallogin.account.extra_data
        print(sociallogin.account.extra_data)
        user = User.objects.create_kakao_user(user_pk=user.pk, extra_data=extra_data)
        return user

