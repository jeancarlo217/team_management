from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Project, Task, UserTask
from django.forms import ModelForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('perfil', 'tipo', 'first_name', 'last_name', 'email')
        labels = {'email': 'Email'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('perfil', 'tipo', 'first_name', 'last_name', 'email')


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': ' '}),
            'description': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': ' '}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'deadline']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': ' '}),
            'description': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': ' '}),
            'status': forms.Select(attrs={'class': 'custom-select', 'id': 'custom-select'}),
            'deadline': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': ' '}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = ''
        
        
class UserTaskForm(ModelForm):
    class Meta:
        model = UserTask
        fields = ['user', 'task']

        widgets = {
            'user': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': ' '}),
            'task': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': ' '}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)