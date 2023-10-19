from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('update-user/<str:pk>/', views.updateuser, name='update-user'),
    path('profile/<str:pk>/', views.userprofile, name='profile'),
    path('create-room/', views.createroom, name='create-room'),
    path('update-room/<str:pk>', views.updateroom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteroom, name='delete-room'),
    path('delete-message/<str:pk>', views.deletemessage, name='delete-message'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('logout/', views.logoutuser, name='logout'),
    path('topics/', views.topicspage, name='topics'),
    path('recent-activity/', views.activitypage, name='recent-activity'),
]
