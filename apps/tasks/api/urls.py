from rest_framework.routers import DefaultRouter    #  Importamos el router de DRF.
from django.urls import path
from ..views import TaskViewSet, RegisterAPIView

router = DefaultRouter()                            #  creamos nuestro router.

router.register(                                    # Le estamos diciendo:  "Router, registra TaskViewSet bajo la ruta tasks."
    r"tasks",
    TaskViewSet,
    basename="task"
)

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register_api"),
]

urlpatterns += router.urls