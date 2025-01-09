# tasks/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField(
        validators=[MinValueValidator(limit_value=timezone.now)],  # Ensure due_date is in the future
    )
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title