import os
import django
from django.db import transaction

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MypreciousWebtoon.settings")
django.setup()

# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from accountApp.models import *


@transaction.atomic
def make_dummy_user():
    user_list = ["heo", 'tae', 'jung', 'owner', 'admin', 'gang', 'seo', 'se']
    email_list = list(map(lambda x: f"{x}@{x}.com", user_list))
    CustomUser.objects.bulk_create([
        CustomUser(email=email, password=1234) for email in email_list
    ])


if __name__ == "__main__":
    make_dummy_user()