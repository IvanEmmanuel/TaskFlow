from django.urls import path
from ..views import TaskListCreateAPIView, TaskRetrieveUpdateDeleteAPIView

urlpatterns = [
    path("tasks/", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskRetrieveUpdateDeleteAPIView.as_view(), name="task-detail")
]