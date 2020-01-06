from django.contrib import admin
from django.urls import path
from . import views

app_name = "webtoonList"

urlpatterns = [
    path('rated_list/', views.Rated, name='Rated'),
    path('rating_list/', views.Rating, name='Rating'),
    path('search_list/', views.Search, name='Search'),
    path('subscribe_list/', views.Subscribe, name='Subscribe'),
    path('random_list/', views.Random, name='Random'),
]