from django import forms
from .models import Libro
from django.core.exceptions import ValidationError
import re
import datetime

class LibroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es un formulario nuevo (sin datos previos), marcamos 'activo' como True
        if not self.instance.pk:
            self.fields['activo'].initial = True

    class Meta:
        model = Libro
        # Listamos los campos que queremos que el usuario llene
        fields = ['titulo', 'autor', 'editorial', 'anio', 'stock', 'activo']
        
        # Etiquetas personalizadas para que se vea bonito en el HTML
        labels = {
            'titulo': 'Título de la Obra',
            'autor': 'Autor',
            'editorial': 'Editorial',   
            'anio': 'Año de Publicación',
            'stock': 'Cantidad Disponible (Stock)',
            'activo': '¿Está Activo?',
        }
        
        # 'widgets' sirve para darle clases de CSS (Bootstrap) a los inputs
        widgets = {
            'titulo': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Ingrese el título del libro'
            }),
            'autor': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del autor'
            }),
            'editorial': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Ingrese la editorial del libro'
            }),
            'anio': forms.NumberInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Ingrese el año de publicación'
            }),
            'stock': forms.NumberInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad disponible en stock'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        # ================= VALIDACIONES =================


    # 1. VALIDAR AUTOR (Solo letras)
    def clean_autor(self):
        autor = self.cleaned_data['autor']
        # Regex: Solo letras y espacios (Igual que en Usuario)
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", autor):
            raise ValidationError("El nombre del autor solo puede contener letras.")
        return autor

    # 2. VALIDAR AÑO (No negativo)
    def clean_anio(self):
        anio = self.cleaned_data['anio']
        if anio < 0:
            raise ValidationError("El año de publicación no puede ser negativo.")

        # Opcional: Validar que no sea del futuro (Ej: año 3000)
        anio_actual = datetime.date.today().year
        if anio > anio_actual:
            raise ValidationError(f"El año no puede ser mayor al actual ({anio_actual}).")

        return anio


    # 3. VALIDAR STOCK (No negativo)
    def clean_stock(self):
        stock = self.cleaned_data['stock']

        if stock < 0:
            raise ValidationError("El stock no puede ser negativo.")

        return stock
