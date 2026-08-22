from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone          # Obtiene la fecha actual para comparar si la tarea ya venció.
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
    
    
    @property  # nos permite acceder a un método del modelo como si fuera un atributo:    {{ task.is_overdue }}   en lugar de:   {{ task.is_overdue() }}
    def is_overdue(self): 
        return self.due_date < timezone.localdate() and self.status != "COMPLETED"      # Una tarea está vencida cuando su fecha límite ya pasó y todavía no está completada.
    
    @property
    def priority_label(self):
        # Devuelve una etiqueta legible según el valor interno de priority.
        if self.priority == "HIGH":
            return "Prioridad alta: esta tarea requiere atención."
        if self.priority == "MEDIUM":
            return "Prioridad media."
        if self.priority == "LOW":
            return "Prioridad baja."
        return ""
    
    @property
    def status_message(self):
        if self.status == "PENDING":
            return "Esta tarea está pendiente."
        if self.status == "IN_PROGRESS":
            return "Esta tarea está en progreso."
        if self.status == "COMPLETED":
            return "Esta tarea está completada."
        return ""
    
    def __str__(self):
        return self.title