# from django.urls import path
# from ..views import TaskListCreateAPIView, TaskRetrieveUpdateDeleteAPIView

# urlpatterns = [
#     path("tasks/", TaskListCreateAPIView.as_view(), name="task-list-create"),
#     path("tasks/<int:pk>/", TaskRetrieveUpdateDeleteAPIView.as_view(), name="task-detail")
# ]

from rest_framework.routers import DefaultRouter
from ..views import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
urlpatterns = router.urls
