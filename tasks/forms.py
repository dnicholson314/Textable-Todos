from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from . import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task name',
                'class': 'task-form-title',
            }),
            'complete': forms.CheckboxInput(attrs={
                'class': 'task-form-complete',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter task description',
                'class': 'task-form-description',
            }),
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'password',
        })

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'username',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'confirm password',
        })