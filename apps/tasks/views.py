from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm

# Create your views here.

def task_list(request):
    tasks = Task.objects.all()
    
    return render(
        request, 
        "tasks/task_list.html",
        {"tasks": tasks}
    )
    
def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
        
    return render(
        request,
        "tasks/task_detail.html",
        {"task": task}
    )
    
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
        
    return render(
        request,
        "tasks/task_form.html",
        {"form": form}
    )
    
def task_edit(request, id):
    task = get_object_or_404(Task, id=id)
    
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
    
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    
    return render(
        request,
        "tasks/task_confirm_delete.html",
        {"task":task}
    )