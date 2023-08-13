from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from monitor.views import MainView, AddInstanceView, DetailInstanceView, SpiderDetailView, JobDetailView
from users.views import register, ProfileView, edit_profile_view
from .views import MainScheduleView, ScheduleDetailView


urlpatterns = [
    path('', MainScheduleView.as_view(), name='schedules_main'),
    path('<int:pk>/', ScheduleDetailView.as_view(), name='schedule_detail'),
]
