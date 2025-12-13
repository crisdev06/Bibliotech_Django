from django.contrib import admin
from .models import Libro

# Esta clase permite personalizar cómo se ve la tabla en el admin
class LibroAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista (columnas de la tabla)
    list_display = ('id_libro', 'titulo', 'autor', 'stock', 'anio')
    # Campos por los que podrás buscar
    search_fields = ('titulo', 'autor', 'id_libro')
    list_filter = ('estado',)

# Registramos el modelo con su configuración
admin.site.register(Libro, LibroAdmin)