from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.signup,name='join'),
    path('login/', views.signin,name='login'),
    ]