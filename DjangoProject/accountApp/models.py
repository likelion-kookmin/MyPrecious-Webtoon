import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from contentsApp.models import Webtoon


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_kakao_user(self, user_pk, extra_data):
        user = CustomUser.objects.get(pk=user_pk)
        profile = user.profile

        # kakao_profile을 기반으로 정보 입력
        kakao_properties = extra_data.get("properties")
        profile.nickname = kakao_properties.get('nickname')
        profile.get_image_from_url(kakao_properties.get('profile_image'))

        kakao_account = extra_data.get("kakao_account")
        profile.gender = 'M' if kakao_account.get('gender') == "male" else 'F'
        age_range = kakao_account.get('age_range').split("~")[0]
        profile.age_range = age_range[:2] if int(age_range) < 60 else 60
        profile.date_of_birth = kakao_account.get('birthday')
        profile.save()
        user.save()

        print(user.profile)
        return user

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # 권한 관련된 부분
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # 순서대로 역참조 방지, 비대칭 관계, 중계모델 설정
    relations = models.ManyToManyField("self", related_name="+",
                                       symmetrical=False, through="Relation")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def following(self):
        # 내가 팔로우 하고 있는 유저들의 목록을 가져온다.
        following_relations = self.relations_by_from_user.all()
        following_pk_list = following_relations.values_list('to_user', flat=True)
        following_users = CustomUser.objects.filter(pk__in=following_pk_list)
        return following_users

    @property
    def followers(self):
        # 나를 팔로우하고 있는 유저들의 목록을 가져온다.
        follower_pk_list = self.relations_by_to_user.values_list('from_user', flat=True)
        follower_users = CustomUser.objects.filter(pk__in=follower_pk_list)
        return follower_users

    def follow(self, to_user):
        if self.id != to_user.id:
            try:
                self.relations_by_from_user.create(to_user=to_user)
                return True
            except django.db.utils.IntegrityError:
                self.relations_by_from_user.filter(to_user=to_user).delete()
                return False


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    AGE_RANGE = (
        (10, "10대"),
        (20, "20대"),
        (30, "30대"),
        (40, "40대"),
        (50, "50대"),
        (60, "60대 이상"),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(blank=True, null=True)
    age_range = models.PositiveSmallIntegerField(blank=True, null=True, choices=AGE_RANGE)
    date_of_birth = models.DateField(blank=True, null=True)
    subscribes = models.ManyToManyField(Webtoon, blank=True)

    def __str__(self):
        return f'{self.nickname} ({self.user.email})'

    def get_image_from_url(self, url):
        from django.core.files.base import ContentFile
        import urllib3, os

        http = urllib3.PoolManager()

        file = http.request('GET', url).data
        file = ContentFile(file)
        filename = os.path.basename(url)
        self.image.save(filename, file)

    def get_values(self):
        from django.forms.models import model_to_dict
        items = model_to_dict(self, fields=[field.name for field in self._meta.fields])
        return items


class Relation(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  # 내가 from_user인 경우 즉 내가 follower인 following한 사람들의 목록을 가져올 때
                                  related_name="relations_by_from_user")
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                # 자신이 to_user인 경우 즉 나의 followee 들의 목록을 가져올 때
                                related_name="relations_by_to_user")

    class Meta:
        unique_together = ("from_user", "to_user",)

    def __str__(self):
        return f'({self.from_user.email} -> {self.to_user.email})'
