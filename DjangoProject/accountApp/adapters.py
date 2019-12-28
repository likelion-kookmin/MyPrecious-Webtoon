from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    pass


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    # social 로그인 시 생성되는 user
    def save_user(self, request, sociallogin, form=None):
        return super().save_user(request, sociallogin, form)

