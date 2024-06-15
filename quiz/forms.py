from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Pregunta, Opcion

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo Electrónico')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

class FormularioInicioSesion(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class FormularioCuestionario(forms.Form):
    def __init__(self, *args, **kwargs):
        preguntas = kwargs.pop('preguntas')
        super(FormularioCuestionario, self).__init__(*args, **kwargs)
        for pregunta in preguntas:
            opciones = [(opcion.id, opcion.texto) for opcion in pregunta.opciones.all()]
            self.fields[f'pregunta_{pregunta.id}'] = forms.ChoiceField(
                choices=opciones,
                widget=forms.RadioSelect,
                label=pregunta.texto,
                required=True
            )
