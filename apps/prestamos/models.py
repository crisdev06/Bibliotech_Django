from django.db import models
from django.core.exceptions import ValidationError
from datetime import date 
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
    
    # Estado del préstamo (Se calculará solo)
    estado_prestamo = models.CharField(
        max_length=20, 
        choices=ESTADOS_PRESTAMO, 
        default='VIGENTE', 
        verbose_name="Estado del Préstamo",
        editable=False # <--- RECOMENDACIÓN: Lo ponemos False para que no se pueda cambiar manualmente en el admin
    )
    
    renovado = models.BooleanField(default=False, verbose_name="¿Fue renovado?")
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?") # Recuerda que cambiamos 'estado' por 'activo' en pasos anteriores

    def __str__(self):
        return f"Préstamo: {self.libro.titulo} - {self.usuario.nombre}"

    def clean(self):
        # Si es un préstamo NUEVO (no tiene ID aún)
        if not self.id:
            # Verificamos si el libro tiene stock disponible
            if self.libro.stock <= 0:
                raise ValidationError(f"Lo sentimos, no queda stock del libro '{self.libro.titulo}'.")

    # --- AQUÍ ESTÁ LA MAGIA ---
    def save(self, *args, **kwargs):
        # --- Lógica de Stock ---
        # Detectamos si es un registro NUEVO (pk es None)
        es_nuevo = self.pk is None
        
        if es_nuevo:
            # Si es nuevo, descontamos 1 al stock del libro
            self.libro.stock -= 1
            self.libro.save() # Guardamos el cambio en la tabla de Libros

        # --- Lógica de Estados (la que ya teníamos) ---
        if self.fecha_devolucion_real:
            self.estado_prestamo = 'DEVUELTO'
        elif self.fecha_devolucion < date.today():
            self.estado_prestamo = 'ATRASADO'
        else:
            self.estado_prestamo = 'VIGENTE'

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"