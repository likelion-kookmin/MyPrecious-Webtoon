import django
from django.db import models
# from accountApp.models import Profile


# Create your models here.
class Webtoon(models.Model):
    image = models.URLField(null=True, blank=True, max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cartoonists = models.ManyToManyField('Cartoonist')
    content_provider = models.ForeignKey('ContentProvider', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', blank=True)
    age_rating = models.ForeignKey('AgeRatingSystem', on_delete=models.PROTECT, default=1)
    url = models.URLField(max_length=200)

    def __str__(self):
        s = [str(i) for i in self.cartoonists.all()]
        return f"{self.name} - {', '.join(s)} by {self.content_provider}"

    def is_all_episode_free(self):
        is_free = True

        for i in Episode.objects.get(webtoon=self):
            if not i.isFree:
                is_free = False
                break
        return is_free


class Cartoonist(models.Model):
    image = models.URLField(null=True, max_length=200)
    name = models.CharField(max_length=100)
    text = models.TextField(null=True)  # 작가의말

    def __str__(self):
        return self.name


class ContentProvider(models.Model):
    image = models.ImageField(null=True, default='')
    name = models.CharField(max_length=100)
    url = models.URLField(default='')

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name


class AgeRatingSystem(models.Model):
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.rating


class Episode(models.Model):
    webtoon = models.ForeignKey('Webtoon', on_delete=models.PROTECT)
    image = models.URLField(default='')
    number = models.IntegerField()
    title = models.TextField()
    created = models.DateField()
    isFree = models.BooleanField()
    url = models.URLField()

    def __str__(self):
        return f"{self.webtoon.name} {[self.number]} \"{self.title}\" ({self.created})"

# class Post(models.Model):
#     author = models.ForeignKey('Profile.User', on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()

#     def __str__(self):
#         return self.title

# class Comment(models.Model):
#     author = models.ForeignKey('Profile.User', on_delete=models.CASCADE)
#     post = models.ForeignKey('Post', related_name='comments', on_delete = models.CASCADE)
#     text = models.TextField()
#     # created_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.text
