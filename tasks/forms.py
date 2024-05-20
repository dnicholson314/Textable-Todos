from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task name',
                'class': 'task-title-input',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter task description',
                'class': 'task-description-input'
            }),
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']