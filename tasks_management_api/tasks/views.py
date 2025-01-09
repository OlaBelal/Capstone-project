from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.decorators import login_required

# Home View
def home(request):
    return render(request, 'tasks/home.html')


# Task List View (Frontend)
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        sort_by = self.request.GET.get('sort')

        if sort_by == 'status':
            queryset = queryset.order_by('status')
        elif sort_by == 'priority':
            queryset = queryset.order_by('priority')
        elif sort_by == 'due_date':
            queryset = queryset.order_by('due_date')

        return queryset


# Task Detail View (Frontend)
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


# Task Create View (Frontend)
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'status']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid! Errors:", form.errors)
        return super().form_invalid(form)


# Task Update View (Frontend)
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'due_date', 'priority', 'status']
    success_url = reverse_lazy('task-list')


# Task Delete View (Frontend)
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# Signup View
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# API Views

# Task List and Create View (API)
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Task Detail View (Retrieve, Update, Delete) (API)
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# Mark Task as Complete View (API)
class MarkTaskCompleteView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        if task.user != request.user:
            return Response({"detail": "You do not have permission to update this task."}, status=403)

        if task.status == 'Pending':
            task.status = 'Completed'
            task.completed_at = timezone.now()
        else:
            task.status = 'Pending'
            task.completed_at = None

        task.save()
        return Response(self.get_serializer(task).data)


# Token Views for JWT Authentication
class TokenObtainPairView(TokenObtainPairView):
    pass


class TokenRefreshView(TokenRefreshView):
    pass


# User Management Views (API)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Task Toggle Status View (Frontend)
class TaskToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['pk'], user=request.user)

        if task.status == 'Pending':
            task.status = 'Completed'
            task.completed_at = timezone.now()
        else:
            task.status = 'Pending'
            task.completed_at = None

        task.save()
        messages.success(request, f'Task "{task.title}" status updated to {task.status}.')
        return redirect('task-list')