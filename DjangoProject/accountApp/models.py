from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
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
    date_of_birth = models.DateField()

    # 권한 관련된 부분
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

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
    MAIL = 1
    FEMAIL = 2
    GENDER_CHOICES = (
        (MAIL, "남자"),
        (FEMAIL, "여자")
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    gender = models.BooleanField(blank=True, null=True, choices=GENDER_CHOICES)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.nickname} ({self.user.email})'


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


