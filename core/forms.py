from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
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
