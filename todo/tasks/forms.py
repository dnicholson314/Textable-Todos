from django import forms

from . import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'