from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )
    
    error_messages = {
        'invalid_login': "Usuario o contraseña incorrectos",
        'inactive': "Esta cuenta está inactiva."
    }
