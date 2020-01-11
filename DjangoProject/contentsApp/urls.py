from django.contrib import admin
from django.urls import path
from . import views

app_name = "contentsApp"

urlpatterns = [
    path('rated_list/', views.Rated, name='rated'),
    path('rating_list/', views.Rating, name='rating'),
    path('search_list/', views.Search, name='search'),
    path('random_list/', views.Random, name='random'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe_list/', views.subscribe_list, name='subscribe_list'),

]