from django import forms
from .models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario', 'fecha_devolucion']

        labels = {
            'libro': 'Libro a prestar',
            'usuario': 'Cliente / Usuario',
            'fecha_devolucion': 'Fecha de Devolución',
        }

        widgets = {
            # ModelChoiceField crea un desplegable automáticamente, le damos estilo Bootstrap
            'libro': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),

            # El truco para el calendario: type="date"
            'fecha_devolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PrestamoSolicitudForm(forms.ModelForm):
    """
    Formulario simplificado para alumnos/profesores.
    Solo muestra Libro y Fecha, el Usuario se asigna en la vista.
    """
    class Meta:
        model = Prestamo
        # SOLO pedimos el libro y la fecha.
        fields = ['libro', 'fecha_devolucion']

        labels = {
            'libro': '¿Qué libro deseas leer?',
            'fecha_devolucion': '¿Cuándo lo devolverás?',
        }

        widgets = {
            'libro': forms.Select(attrs={'class': 'form-select'}),
            'fecha_devolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    # Filtramos para que solo aparezcan libros con stock disponible
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra los libros que tengan stock mayor a 0 y estén activos
        self.fields['libro'].queryset = self.fields['libro'].queryset.filter(stock__gt=0, activo=True)
