from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import User

class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'document_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit: user.save()
        return user