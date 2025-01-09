from rest_framework import serializers
from .models import Task
from datetime import datetime
from django.contrib.auth.models import User

#tasks

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'user', 'completed_at']
        read_only_fields = ['user', 'completed_at']
    def validate_due_date(self, value):
        if value < datetime.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

#user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in responses

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
