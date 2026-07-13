from django.db import models
# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']  


class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    id_libro = models.CharField( verbose_name="ID Libro", max_length=13, unique=True,)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    editorial = models.CharField(max_length=100)
    anio = models.IntegerField(verbose_name="Año")
    stock = models.IntegerField()
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")
    categoria = models.ForeignKey(
    Categoria,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    verbose_name="Categoría"
    )


  
    def __str__(self):
        return str(self.titulo)

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

    