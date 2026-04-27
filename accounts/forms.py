from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User, Address

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

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'neighborhood', 'city', 'reference']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'document_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'document_number': forms.TextInput(attrs={'placeholder': 'Documento'}),
        }