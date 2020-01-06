from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # accounts/로 이동
    # path('signup/', views.signupView, name='signup'),
    # path('login/', views.loginView, name='login'),
    path('', views.userListView, name='user_list'),
    path('logout/', views.logoutView, name='logout'),
    path('reset/', views.deleteUsers, name="reset"),
    path('follow/', views.follow, name="follow"),

    # profile에서 follower, following 목록으로
    path('profile/', views.profile, name="profile"),
    path('follow-list/', views.followListView, name="follow_list")
]
