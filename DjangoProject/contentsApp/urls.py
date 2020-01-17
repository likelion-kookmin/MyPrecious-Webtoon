from django.contrib import admin
from django.urls import path
from . import views

app_name = "contentsApp"

urlpatterns = [
    path('search_list/', views.Search, name='search'),
    path('random_list/', views.Random, name='random'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('rate/', views.subscribe, name='Rate'),
    path('subscribe_list/', views.subscribe_list, name='subscribe_list'),
    path('detail/<int:id>', views.webtoon_detail, name='detail'),
    path('comment/<int:id>/create', views.comment_create, name="comment_create"),
    path('comment/<int:id>/delete', views.comment_delete, name="comment_delete"),
    path('tag_list/', views.tag_list, name="tag_list"),
    path('<int:id>/review', views.review, name="review"),

]