from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

class TaskListView(LoginRequiredMixin, ListView): # heredamos de las c lases padres LoginRequiredMixin, ListView
                                                  # LoginRequiredMixin hace lo que anteriormente hacíamos con: @login_required
    model = Task                                  # Esta vista trabaja con el modelo Task.
    template_name = "tasks/task_list.html"        # Le indicamos qué template debe renderizar.
    context_object_name = "tasks"                 # Proporciona un nombre basado en el modelo
    
    def get_queryset(self):
        return Task.objects.filter(               # Aquí estamos conservando nuestra regla de autorización, solo trae los registros del usuario autenticado.
            user=self.request.user
        )


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





##############################################################
#                Antiguas FBV(Function Base Views)
##############################################################
# Existen estas dos formas de hacerlo pero la mas recomendada es CBV

#FBV	                |         CBV
#@login_required	        LoginRequiredMixin
#render()	                comportamiento de Generic View
#get_object_or_404()	    DetailView / UpdateView / DeleteView
#request.user	            self.request.user
#form.is_valid()	        form_valid()
#redirect()	                success_url
#consulta filtrada	        get_queryset()


@login_required
def task_list(request):    # -> function base view antiguo, ahora usaremos TaskListView
    # tasks = Task.objects.all()    ->     obtiene todas las tareas de todos los usuarios
    tasks = Task.objects.filter(user=request.user)  # obtiene solo las tareas de el usuario autenticado
    
    
    return render(
        request, 
        "tasks/task_list.html",
        {"tasks": tasks}
    )

@login_required 
def task_detail(request, id):
    # task = get_object_or_404(Task, id=id)   ->  obtenia la informacion de una tarea, osea los detalles
    task = get_object_or_404(Task, id=id, user=request.user) #  obtiene la tarea seleccionada de ese usuario autenticado que le pertenesca
        
    return render(
        request,
        "tasks/task_detail.html",
        {"task": task}
    )

@login_required    
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False) # detiene el guardado a la bd y lo guarda en memoria
            task.user = request.user # asigna el usuario quie creo la tarea
            form.save() # guarda en bd
            
            messages.success( # importamos la libreria messages y enviamos un mensage de confirmacion al template
                request,
                "Tarea creada correctamente."
            )
            
            return redirect("tasks:task_list")
    else:
        form = TaskForm()
        
    return render(
        request,
        "tasks/task_form.html",
        {"form": form}
    )

@login_required    
def task_edit(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)  #  obtiene la tarea seleccionada de ese usuario autenticado que le pertenesca
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            form.save()
            
            messages.success(
                request,
                "Tarea actualizada correctamente.",
            )
            return redirect("tasks:task_detail", id=task.id)
        
    else:
        form = TaskForm(instance=task)
        
    return render(
        request,
        "tasks/task_form.html",
        {"form":form}
    )

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user) #  obtiene la tarea seleccionada de ese usuario autenticado que le pertenesca
    
    if request.method == "POST":
        task.delete()
        
        messages.success(
            request,
            "Tarea eliminada correctamente."
        )
        return redirect("tasks:task_list")
    
    return render(
        request,
        "tasks/task_confirm_delete.html",
        {"task":task}
    )