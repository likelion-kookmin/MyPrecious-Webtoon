from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Webtoon)
admin.site.register(Cartoonist)
admin.site.register(ContentProvider)
admin.site.register(Tag)
admin.site.register(RatingSystem)
admin.site.register(Episode)