from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    # Mostramos RUT, nombre, tipo (Estudiante/Docente) y correo
    list_display = ('rut', 'nombre', 'apellido', 'tipo', 'correo')
    # Filtros laterales para buscar rápido por tipo (Estudiante vs Docente)
    list_filter = ('tipo', 'estado')
    search_fields = ('rut', 'nombre', 'apellido')

admin.site.register(Usuario, UsuarioAdmin)