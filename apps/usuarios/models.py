# Create your models here.
from django.db import models

class Usuario(models.Model):
    # Definimos las opciones para el tipo de usuario
    TIPO_USUARIO = [
        ('ESTUDIANTE', 'Estudiante'),
        ('DOCENTE', 'Docente'),
        ('ADMINISTRATIVO', 'Administrativo'),
    ]

    rut = models.CharField(primary_key=True, max_length=12, unique=True, verbose_name="RUT")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    correo = models.EmailField()
    password = models.CharField(max_length=128)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, verbose_name="Tipo de Usuario")
    estado = models.BooleanField(default=True, verbose_name="¿Está activo?")

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"