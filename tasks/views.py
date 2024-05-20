from django.shortcuts import render, redirect
from django.urls import reverse
from . import models, forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.http import HttpResponseForbidden

class TaskLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

@login_required
def index(request):
    if request.method == "POST":
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

        return redirect(reverse('list'))
    else:
        tasks = models.Task.objects.filter(user=request.user)
        form = forms.TaskForm

    context = {
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'tasks/list.html', context)

def register(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list')
    else:
        form = forms.SignUpForm()
        print(form.fields)

    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


# pk comes from the url pattern
@login_required
def update_task(request, pk):
    task = models.Task.objects.get(id=pk)
    if task.user != request.user:
        return HttpResponseForbidden("The user does not have permission to access this task.")

    if request.method == "POST":
        form = forms.TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect(reverse('list'))

    form = forms.TaskForm(instance=task)
    context = {
        'form': form
    }

    return render(request, "tasks/update_task.html", context)

@login_required
def delete_task(request, pk):
    task = models.Task.objects.get(id=pk)
    if task.user != request.user:
        return HttpResponseForbidden("The user does not have permission to access this task.")

    if request.method == "POST":
        task.delete()
        return redirect(reverse('list'))

    context = {
        "task": task,
    }
    return render(request, 'tasks/delete_task.html', context)