from django.db import models

# Create your models here.
class Webtoon(models.Model):
    image = models.ImageField(null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    cartoonists = models.ManyToManyField('Cartoonist')
    content_provider = models.ForeignKey('ContentProvider', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag')
    age_rating = models.ForeignKey('RatingSystem', on_delete=models.PROTECT, default=1)
    url = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - "

class Cartoonist(models.Model):
    image = models.ImageField(null=True)
    name = models.CharField(max_length=100)
    text = models.TextField(null=True) # 작가의말

    def __str__(self):
        return self.name

class ContentProvider(models.Model):
    image = models.ImageField(null=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name

class RatingSystem(models.Model):
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.rating

class Episode(models.Model):
    webtoon = models.ForeignKey('Webtoon', on_delete=models.PROTECT)
    image = models.ImageField()
    number = models.IntegerField()
    title = models.TextField()
    created = models.DateField()
    isFree = models.BooleanField()

    url = models.CharField(max_length=100)