from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

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
        fields = ['street', 'neighborhood', 'municipality', 'reference']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'document_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'document_number': forms.TextInput(attrs={'placeholder': 'Documento'}),
        }

class StaffUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'document_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'document_number': forms.TextInput(attrs={'placeholder': 'Documento'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-5 py-4 rounded-2xl bg-gray-50 border-2 border-transparent focus:border-orange-500 focus:bg-white outline-none transition-all font-bold text-gray-900',
                'placeholder': field.label
            })