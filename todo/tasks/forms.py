from django import forms

from . import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter task name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter task description'})
        }