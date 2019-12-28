from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_kakao_user(self, user_pk, extra_data):
        user = CustomUser.objects.get(pk=user_pk)
        profile = user.profile

        # kakao_profile을 기반으로 정보 입력
        kakao_properties = extra_data.get("properties")
        profile.nickname = kakao_properties.get('nickname')
        profile.get_image_from_url(kakao_properties.get('thumbnail_image'))

        kakao_account = extra_data.get("kakao_account")
        profile.gender = 'M' if kakao_account.get('gender') == "male" else 'F'
        age_range = kakao_account.get('age_range')
        profile.age_range = age_range[:2] if age_range else age_range
        print(age_range)
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


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    AGE_RANGE = (
        (10, "10"),
        (20, "20"),
        (30, "30"),
        (40, "40"),
        (50, "50"),
        (60, "60"),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    gender = models.CharField(blank=True, null=True, max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(blank=True, null=True)
    age_range = models.CharField(blank=True, null=True, max_length=2, choices=AGE_RANGE)
    date_of_birth = models.DateField(blank=True, null=True)

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
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])


# allauth adapter로 처리
# @receiver(post_save, sender=CustomUser)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
