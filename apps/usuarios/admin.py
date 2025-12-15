from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','rut', 'nombre', 'apellido', 'correo','password','tipo', 'activo')
    # Filtros laterales para buscar rápido por tipo (Estudiante vs Docente)
    list_filter = ('tipo', 'activo')
    search_fields = ('rut', 'nombre', 'apellido')

admin.site.register(Usuario, UsuarioAdmin)
