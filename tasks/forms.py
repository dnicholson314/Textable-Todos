from django import forms

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