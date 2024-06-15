from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pregunta(models.Model):
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class Resultado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    es_correcta = models.BooleanField()

    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.texto}"