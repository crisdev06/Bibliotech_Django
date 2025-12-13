from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        # Listamos los campos que queremos que el usuario llene
        fields = ['id_libro', 'titulo', 'autor', 'editorial', 'anio', 'stock']
        
        # Etiquetas personalizadas para que se vea bonito en el HTML
        labels = {
            'id_libro': 'Código del Libro (ID)',
            'titulo': 'Título de la Obra',
            'autor': 'Autor',
            'editorial': 'Editorial',   
            'anio': 'Año de Publicación',
            'stock': 'Cantidad Disponible (Stock)',
        }
        
        # 'widgets' sirve para darle clases de CSS (Bootstrap) a los inputs
        widgets = {
            'id_libro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: LIB001'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }