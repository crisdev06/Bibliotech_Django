from django.contrib import admin
from .models import Prestamo

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion', 'estado_prestamo', 'activo')
    list_filter = ('estado_prestamo', 'fecha_prestamo', 'activo')
    search_fields = ('usuario__nombre', 'usuario__rut', 'libro__titulo')

admin.site.register(Prestamo, PrestamoAdmin)