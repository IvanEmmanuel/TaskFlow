from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("<int:id>/", views.task_detail, name="task_detail"),
    path("create/", views.task_create, name="task_create"),
    path("<int:id>/edit/", views.task_edit, name="task_edit"),
    path("<int:id>/delete/", views.task_delete, name="task_delete"),
]