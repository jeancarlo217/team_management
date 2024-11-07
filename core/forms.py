from django.forms import ModelForm
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('perfil', 'tipo', 'first_name', 'last_name')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]

        if commit:
            user.save()

        return user
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('perfil', 'tipo', 'first_name', 'last_name')
