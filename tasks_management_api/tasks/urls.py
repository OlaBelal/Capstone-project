from django.contrib import admin
from django.urls import path, include
from .views import TaskToggleStatusView
from tasks.views import (
    home, TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    TaskListCreateView, MarkTaskCompleteView, SignUpView,
    UserListCreateView, UserRetrieveUpdateDestroyView  # Add the new user views
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Front-end URLs
frontend_urlpatterns = [
    path('', home, name='home'),  # Home page
    path('tasks/', TaskListView.as_view(), name='task-list'),  # Task list (front-end)
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),  # Create task (front-end)
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),  # Task detail (front-end)
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),  # Update task (front-end)
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),  # Delete task (front-end)
]

# API URLs
api_urlpatterns = [
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),  # List and create tasks (API)
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),  # Retrieve, update, and delete tasks (API)
    path('api/tasks/<int:pk>/complete/', MarkTaskCompleteView.as_view(), name='task-complete'),  # Mark task as complete (API)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT Token Obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT Token Refresh
]

# User Management URLs
user_urlpatterns = [
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),  # List and create users (API)
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),  # Retrieve, update, and delete users (API)
]

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Add Django's authentication URLs
    path('accounts/signup/', SignUpView.as_view(), name='signup'),  # Signup page
    path('tasks/<int:pk>/toggle-status/', TaskToggleStatusView.as_view(), name='task-toggle-status'),
] + frontend_urlpatterns + api_urlpatterns + user_urlpatterns  # Combine all URL patterns