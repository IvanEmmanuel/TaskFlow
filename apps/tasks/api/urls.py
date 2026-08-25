# from django.urls import path            #  Importamos path() para definir nuestra URL.

# from ..views import TaskListAPIView, TaskDetailAPIView     #  Estamos importando nuestra vista: apps/tasks/views.py ->  TaskListAPIView, TaskDetailAPIView

# urlpatterns = [
#     path("tasks/", TaskListAPIView.as_view(), name="task-list",),               # Cuando alguien solicite tasks/, ejecuta TaskListAPIView.
#     path("tasks/<int:pk>/", TaskDetailAPIView.as_view(), name="task-detail"),
# ]

from rest_framework.routers import DefaultRouter    #  Importamos el router de DRF.

from ..views import TaskViewSet

router = DefaultRouter()                            #  creamos nuestro router.

router.register(                                    # Le estamos diciendo:  "Router, registra TaskViewSet bajo la ruta tasks."
    r"tasks",
    TaskViewSet,
    basename="task"
)

urlpatterns = router.urls
