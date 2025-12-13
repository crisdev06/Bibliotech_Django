from django.db import models
from apps.usuarios.models import Usuario
from apps.libros.models import Libro

class Prestamo(models.Model):
    ESTADOS_PRESTAMO = [
        ('VIGENTE', 'Vigente'),
        ('DEVUELTO', 'Devuelto'),
        ('ATRASADO', 'Atrasado'), 
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    # Fechas
    fecha_prestamo = models.DateField(auto_now_add=True, verbose_name="Fecha de Préstamo")
    fecha_devolucion = models.DateField(verbose_name="Fecha de Devolución Estimada")
    fecha_devolucion_real = models.DateField(null=True, blank=True, verbose_name="Fecha de Devolución Real")
    # Control para la regla de "una única renovación"
    estado_prestamo = models.CharField(
        max_length=20, 
        choices=ESTADOS_PRESTAMO, 
        default='VIGENTE', 
        verbose_name="Estado del Préstamo"
    )
    renovado = models.BooleanField(default=False, verbose_name="¿Fue renovado?")
    estado = models.BooleanField(default=True, verbose_name="¿Está activo?")

    def __str__(self):
        return f"Préstamo: {self.libro.titulo} - {self.usuario.nombre}"

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"