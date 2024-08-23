from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario', max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
