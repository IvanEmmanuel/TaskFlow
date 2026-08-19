from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATUS_CHOICES = [
    ("PENDING", "Pendiente"),
    ("IN_PROGRESS", "En progreso"),
    ("COMPLETED", "Completado"),
]

PRIORITY_CHOICES = [
    ("LOW", "Bajo"),
    ("MEDIUM", "Medio"),
    ("HIGH", "Alto"),
]

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=7, choices=PRIORITY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    
    def __str__(self):
        return self.title