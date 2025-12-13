from django.db import models
# Create your models here.

class Libro(models.Model):
    id_libro = models.CharField(primary_key=True, verbose_name="ID Libro", max_length=13)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    anio = models.IntegerField(verbose_name="Año")
    stock = models.IntegerField()
    estado = models.BooleanField(default=True, verbose_name="¿Está activo?")
    # Opcional: Para que en el admin se vea el nombre del libro en vez de "Libro object"
    def __str__(self):
        return str(self.titulo)

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"