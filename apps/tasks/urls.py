from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("<int:id>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
    path("<int:id>/edit/", views.TaskUpdateView.as_view(), name="task_edit"),
    path("<int:id>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
]