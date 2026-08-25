import django_filters

from .models import Task, STATUS_CHOICES, PRIORITY_CHOICES


class TaskFilter(django_filters.FilterSet):

    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        label="Estado",
        help_text="Filtrar tareas por estado.",
    )

    priority = django_filters.ChoiceFilter(
        choices=PRIORITY_CHOICES,
        label="Prioridad",
        help_text="Filtrar tareas por prioridad.",
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "priority",
        ]