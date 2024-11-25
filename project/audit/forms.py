from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Role, Cycle

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label='Cargo')
    cycle = forms.ModelChoiceField(queryset=Cycle.objects.all(), label='Año', empty_label='Seleccione un ciclo')

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'cycle']
