from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.utils import timezone

# Create your views here.


# View encargada de registrar un nuevo usuario.
def register(request):
    
    # Si el usuario ya está autenticado, lo enviamos directamente a sus tareas.
    if request.user.is_authenticated:
        return redirect("tasks:task_list")

    # Comprobamos si el usuario envió el formulario.
    if request.method == "POST":

        # RegisterForm es nuestro formulario personalizado.(revisar forms.py)
        # Hereda de UserCreationForm de Django y agrega el campo email.
        # request.POST contiene los datos enviados por el usuario.
        form = RegisterForm(request.POST)

        # Ejecutamos las validaciones definidas por RegisterForm, es decir que todo venga bien
        # y por su clase padre UserCreationForm.
        if form.is_valid():

            # Guarda el nuevo usuario en la base de datos
            # y devuelve el objeto User creado.
            user = form.save()

            # Autentica automáticamente al usuario recién creado.
            # Así no tiene que iniciar sesión manualmente después del registro.
            login(request, user)

            # Redirige al usuario a la lista de tareas después
            # de completar correctamente el registro.
            return redirect("tasks:task_list")

    else:

        # Si la petición es GET, creamos un formulario vacío
        # para mostrarlo al usuario.
        form = RegisterForm()

    # Renderiza el template de registro y le envía el formulario.
    return render(
        request,
        "registration/register.html",
        {"form": form}
    )

class TaskListView(LoginRequiredMixin, ListView):   # heredamos de las c lases padres LoginRequiredMixin, ListView
                                                    # LoginRequiredMixin hace lo que anteriormente hacíamos con: @login_required
    model = Task                                    # Esta vista trabaja con el modelo Task.
    template_name = "tasks/task_list.html"          # Le indicamos qué template debe renderizar.
    context_object_name = "tasks"                   # Proporciona un nombre basado en el modelo
    paginate_by = 5                                 # Mostrar máximo 5 tareas por página.
    
    # Conjunto de estados válidos que el usuario puede utilizar como filtro.
    # Evita aceptar valores de estado que no estén contemplados por la aplicación. ->  /tasks/?status=HACK
    VALID_STATUSES = {
        "PENDING",
        "IN_PROGRESS",
        "COMPLETED",
    }

    # Conjunto de prioridades válidas que el usuario puede utilizar como filtro.
    # Se utiliza para validar el parámetro "priority" recibido desde la URL.
    VALID_PRIORITIES = {
        "LOW",
        "MEDIUM",
        "HIGH",
    }

    # Conjunto de opciones válidas para ordenar las tareas.
    # Define los valores que puede recibir el parámetro "order" desde la URL.
    VALID_ORDERS = {
        "due_asc",
        "due_desc",
        "newest",
        "oldest",
    }
    
    
    def get_queryset(self): # se encarga de determinar qué tareas aparecen en la lista.

        # Primero obtenemos únicamente las tareas del usuario autenticado y se las asignamos a queryset.
        queryset = Task.objects.filter(
            user=self.request.user
        )

        # Aquí estamos conservando nuestra regla de autorización, solo trae los registros del usuario autenticado.

        return self.apply_filters(queryset)  # Enviamos el QuerySet(queryset) a apply_filters() para aplicar los filtros y devolver el resultado final.


    def get_context_data(self, **kwargs): # se encarga de agregar información adicional que queremos enviar al template.
        
        context =super().get_context_data(**kwargs)     # Obtenemos el contexto que Django prepara normalmente para el template.

        # Obtenemos todas las tareas del usuario autenticado,
        # sin aplicar los filtros de búsqueda, estado, prioridad u ordenamiento.
        user_tasks = Task.objects.filter(
            user=self.request.user
        )
        
        context["total_tasks"] = user_tasks.count()         # Contamos todas las tareas pertenecientes al usuario.
        
        context["pending_tasks"] = user_tasks.filter(       # Contamos únicamente las tareas que están pendientes.
            status="PENDING"
        ).count()
        
        context["in_progress_tasks"] = user_tasks.filter(   # Contamos las tareas que están actualmente en progreso.
            status="IN_PROGRESS"
        ).count()
        
        context["completed_tasks"] = user_tasks.filter(     # Contamos las tareas que ya fueron completadas.
            status="COMPLETED"
        ).count()
        
        # Contamos las tareas vencidas.
        # Una tarea se considera vencida cuando su fecha límite ya pasó
        # y todavía no está completada.
        context["overdue_tasks"] = user_tasks.filter(
            due_date__lt=timezone.now().date(),
        ).exclude(
            status="COMPLETED"
        ).count()
        
        return context                                      # Devolvemos el contexto para que esté disponible en task_list.html.
    

    def apply_filters(self, queryset):                  # Aquí recibimos: queryset, que ya contiene únicamente las tareas del usuario autenticado.

        # Filtrado por búsqueda por título.
        search = self.request.GET.get("search")         # Obtenemos el texto que el usuario escribió en el parámetro search o buscador.

        if search:                                      # Comprobamos si realmente se proporcionó un texto de búsqueda, es decir, que no venga vacío.
            queryset = queryset.filter(
                title__icontains=search                 # Filtramos el QuerySet para conservar títulos que contengan el texto, ignorando mayúsculas y minúsculas.
            )

        # Filtrado por estado.
        status = self.request.GET.get("status")         # Obtenemos el estado que el usuario seleccionó desde el formulario.

        if status in self.VALID_STATUSES:               # Comprobamos si el usuario realmente seleccionó un estado.
            queryset = queryset.filter(
                status=status                           # Filtramos el QuerySet comparando el estado de la tarea con el valor enviado por el usuario.
            )

        # Filtrado por prioridad.
        priority = self.request.GET.get("priority")     # Obtenemos la prioridad que el usuario seleccionó desde el formulario.

        if priority in self.VALID_PRIORITIES:           # Comprobamos si el usuario realmente seleccionó una prioridad.
            queryset = queryset.filter(
                priority=priority                       # Filtramos el QuerySet comparando la prioridad de la tarea con el valor enviado por el usuario.
            )

        # Ordenamiento de las tareas.
        order = self.request.GET.get("order")           # Obtenemos el tipo de ordenamiento que el usuario seleccionó.

        if order in self.VALID_ORDERS:                      # Obtenemos el tipo de ordenamiento que el usuario seleccionó.
        
            if order == "due_asc":                          # Comprobamos si el usuario quiere ordenar por fecha límite ascendente.
                queryset = queryset.order_by("due_date")    # Ordenamos las tareas de la fecha límite más próxima a la más lejana.

            elif order == "due_desc":                       # Comprobamos si el usuario quiere ordenar por fecha límite descendente.
                queryset = queryset.order_by("-due_date")   # Ordenamos las tareas de la fecha límite más lejana a la más próxima.

            elif order == "newest":                         # Comprobamos si el usuario quiere ver primero las tareas más recientes.
                queryset = queryset.order_by("-created_at") # El signo "-" indica orden descendente, por lo que las más recientes aparecen primero.

            elif order == "oldest":                         # Comprobamos si el usuario quiere ver primero las tareas más antiguas.
                queryset = queryset.order_by("created_at")  # Ordenamos las tareas desde la más antigua hasta la más reciente.


        return queryset                                 # Devolvemos el QuerySet final después de aplicar los filtros y el ordenamiento.
 

class TaskDetailView(LoginRequiredMixin, DetailView):
    
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    pk_url_kwarg = "id"                                 #  ¿Cómo se llama el parámetro de la URL que contiene el identificador? es para la url
    
    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user
        )


class TaskCreateView(LoginRequiredMixin, CreateView):   # LoginRequiredMixin exige que el usuario esté autenticado para acceder a esta vista.
    
    model = Task                                        # Indica que esta vista trabajará con el modelo Task.
    form_class = TaskForm                               # Indica que CreateView utilizará nuestro TaskForm para crear y validar la tarea.
    template_name = "tasks/task_form.html"              # Indica el template que se utilizará para mostrar el formulario.
    success_url = reverse_lazy("tasks:task_list")             # Indica a qué URL se redirigirá al usuario después de crear correctamente la tarea.

    def form_valid(self, form):                         # Se ejecuta automáticamente cuando el formulario pasó todas las validaciones.
        task = form.save(commit=False)                  # Crea el objeto Task en memoria, pero todavía no lo guarda en la base de datos.
        task.user = self.request.user                   # Asigna automáticamente la tarea al usuario que está actualmente autenticado.
        task.save()                                     # Guarda la tarea en la base de datos después de asignarle el usuario.

        messages.success(
            self.request,
            "Tarea creada correctamente.",              # Guarda un mensaje temporal de éxito para mostrarlo después del redirect.
        )                                               

        return super().form_valid(form)                 # Continúa con el comportamiento normal de CreateView después de nuestra lógica personalizada.


class TaskUpdateView(LoginRequiredMixin, UpdateView):   # Exige que el usuario esté autenticado para acceder a esta vista.
    model = Task                                        # Indica que la vista trabajará con el modelo Task.
    form_class = TaskForm                               # Indica que utilizaremos nuestro TaskForm para editar la tarea.
    template_name = "tasks/task_form.html"              # Indica el template que mostrará el formulario de edición.
    context_object_name = "task"                        # Define el nombre con el que la tarea estará disponible dentro del template.
    success_url = reverse_lazy("tasks:task_list")             # Indica a dónde se redirigirá después de actualizar correctamente.
    pk_url_kwarg = "id"                                 # Indica que el identificador de la tarea viene en la URL con el nombre id.
    
    def get_queryset(self):                             # Define qué tareas puede encontrar y editar esta vista.
        return Task.objects.filter(
            user= self.request.user                     # Limita la consulta a las tareas pertenecientes al usuario autenticado.
        )
    
    def form_valid(self, form):                         # Se ejecuta cuando el formulario pasó todas las validaciones.
        messages.success(
            self.request,
            "Tarea actualizada correctamente.",         # Guarda un mensaje temporal indicando que la tarea fue actualizada.
        )
        
        return super().form_valid(form)                 # Continúa con el comportamiento normal de UpdateView y guarda la instancia.

class TaskDeleteView(LoginRequiredMixin, DeleteView):   # Exige que el usuario esté autenticado para acceder a esta vista.
    model = Task                                        # Indica que la vista trabajará con el modelo Task.
    template_name = "tasks/task_confirm_delete.html"    # Indica el template que mostrará la confirmación antes de eliminar.
    success_url = reverse_lazy("tasks:task_list")             # Indica a dónde se redirigirá después de eliminar correctamente.
    pk_url_kwarg = "id"                                 # Indica que el identificador de la tarea viene en la URL con el nombre id.
    
    def get_queryset(self):                             # Define qué tareas puede encontrar y eliminar esta vista.
        return Task.objects.filter(
            user = self.request.user                    # Limita la consulta a las tareas pertenecientes al usuario autenticado.
        )
        
    def form_valid(self, form):                         # Se ejecuta cuando el usuario confirma la eliminación mediante POST.
        messages.success(
            self.request,
            "Tarea eliminada correctamente."            # Guarda un mensaje temporal indicando que la tarea fue eliminada.
        )
        
        return super().form_valid(form)                 # Continúa con el comportamiento normal de DeleteView y elimina la tarea.
    

###   -------------------------------------------------------------------------
###                        API
###   -------------------------------------------------------------------------

