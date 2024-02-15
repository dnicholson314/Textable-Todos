from django.shortcuts import render, redirect
from . import models, forms

def index(request):
    if request.method == "POST":
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    tasks = models.Task.objects.all()
    form = forms.TaskForm
    context = {
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'tasks/list.html', context)

# pk comes from the url pattern
def update_task(request, pk):
    task = models.Task.objects.get(id=pk)

    if request.method == "POST":
        form = forms.TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    form = forms.TaskForm(instance=task)
    context = {
        'form': form
    }

    return render(request, "tasks/update_task.html", context)

def delete_task(request, pk):
    task = models.Task.objects.get(id=pk)

    if request.method == "POST":
        task.delete()
        return redirect('/')

    context = {
        "task": task,
    }
    return render(request, 'tasks/delete_task.html', context)