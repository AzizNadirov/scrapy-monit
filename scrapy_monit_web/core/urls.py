from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from monitor.views import MainView, AddInstanceView, DetailInstanceView, SpiderDetailView, JobDetailView
from users.views import register, ProfileView, edit_profile_view



urlpatterns = [
    path('admin/', admin.site.urls),
    # home
    path('', MainView.as_view(), name='main'),
    # auth
    path('register/', register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'users/login.html'), name = "login"),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = "logout"),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('profedit/', edit_profile_view, name = 'edit_profile'),
    # CRUD instance
    path('add/', AddInstanceView.as_view(), name = 'add_instance'),
    path('instance/<str:name>/', DetailInstanceView.as_view(), name = 'instance_detail'),
    path('instance/<str:name>/<str:spider_name>/', SpiderDetailView.as_view(), name = 'spider_detail'),
    path('instance/<str:instance_name>/<str:spider_name>/<str:job_id>/', JobDetailView.as_view(), name = 'job_detail'),
    path('schedules/', include('schedules.urls')),
    path('api/', include('api.urls')),

]
