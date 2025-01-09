"""
URL configuration for tasks_management_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# tasks_management_api/urls.py
from django.contrib import admin
from django.urls import path, include
from tasks.views import (
    home, TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    TaskListCreateView, MarkTaskCompleteView, SignUpView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),  # Include your app's URLs
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),  # Add Django's authentication URLs
    path('accounts/signup/', SignUpView.as_view(), name='signup'),  # Signup page
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('', home, name='home'),
    path('tasks/', include('tasks.urls')),
   

]



