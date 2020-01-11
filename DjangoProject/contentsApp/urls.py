from django.contrib import admin
from django.urls import path
from . import views

app_name = "contents"

urlpatterns = [
    path('detail/<int:id>', views.webtoon_detail, name='detail'),
    
]
