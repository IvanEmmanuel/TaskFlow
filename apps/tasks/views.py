from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def task_list(request):
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
            return redirect("task_list")
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
            return redirect("task_detail", id=task.id)
        
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
        return redirect("task_list")
    
    return render(
        request,
        "tasks/task_confirm_delete.html",
        {"task":task}
    )