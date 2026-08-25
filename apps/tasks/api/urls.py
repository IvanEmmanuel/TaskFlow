from django.urls import path            #  Importamos path() para definir nuestra URL.

from ..views import TaskListAPIView, TaskDetailAPIView     #  Estamos importando nuestra vista: apps/tasks/views.py ->  TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path("tasks/", TaskListAPIView.as_view(), name="task-list",),               # Cuando alguien solicite tasks/, ejecuta TaskListAPIView.
    path("tasks/<int:pk>/", TaskDetailAPIView.as_view(), name="task-detail"),
]