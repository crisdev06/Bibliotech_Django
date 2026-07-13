from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re



class UsuarioForm(forms.ModelForm):

    terminos_condiciones = forms.BooleanField(
        required=True,
        label='Acepto los Términos y Condiciones de uso de la plataforma.',
        error_messages={'required': 'Debes aceptar los Términos y Condiciones para registrarte.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    uso_datos = forms.BooleanField(
        required=True,
        label='Autorizo el tratamiento de mis datos personales conforme a la Ley 21.719 de Protección de Datos Personales.',
        error_messages={'required': 'Debes autorizar el uso de tus datos personales para registrarte.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        # 1. Extraemos el usuario que pasamos desde la vista
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Si el usuario NO existe (registro público) o NO es superusuario...
        if not self.user or not self.user.is_superuser:
            # Limitamos las opciones a solo Estudiante y Docente
            self.fields['tipo'].choices = [
                ('ESTUDIANTE', 'Estudiante'),
                ('DOCENTE', 'Docente'),
            ]

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'telefono', 'correo','password', 'tipo', 'terminos_condiciones', 'uso_datos']
        labels = {
            'nombre': 'Nombres',
            'apellido': 'Apellido',
            'rut': 'RUT',
            'telefono': 'Teléfono de Contacto',
            'correo': 'Correo Electrónico',
            'password': 'Contraseña',
            'tipo': 'Tipo de Usuario',
            'terminos_condiciones': 'Acepto los Términos y Condiciones de uso de la plataforma.',
            'uso_datos': 'Autorizo el tratamiento de mis datos personales conforme a la Ley 19.628 y sus modificaciones vigentes sobre protección de la vida privada.',
        }

        widgets = {
            'nombre': 
            forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'ingrese su nombre'}),
            'apellido': 
            forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder': 'Ingrese su apellido'}),
            'rut':
              forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su RUT'}),
            'telefono': 
            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su teléfono'}),
            'correo': 
            forms.EmailInput(attrs={'class': 'form-control',
                                     'placeholder': 'Ingrese su correo electrónico'}),
            'password':
              forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Ingrese su contraseña'}),
            'tipo': 
            forms.Select(attrs={'class': 'form-select'}),
        }
# ================= VALIDACIONES =================

    # VALIDACIÓN 1: RUT (Formato y Matemática)
    def clean_rut(self):
        rut = self.cleaned_data['rut']

        # A. Validación de Duplicados (Login y Negocio)
        if User.objects.filter(username=rut).exists():
            raise ValidationError("Este RUT ya tiene un usuario de sistema creado.")
        if Usuario.objects.filter(rut=rut).exists():
            raise ValidationError("Este RUT ya está registrado como cliente.")

        # B. Validación de Formato (Ej: 12345678-9)
        # Debe tener números, un guion y terminar en número o K
        if not re.match(r'^\d{7,8}-[\dkK]$', rut):
            raise ValidationError("El formato debe ser sin puntos y con guion. Ej: 11111111-1")

        # C. Validación Matemática (Algoritmo Chileno)
        try:
            rut_cuerpo, dv_ingresado = rut.split("-") # Separamos 11111111 de 1
            rut_cuerpo = int(rut_cuerpo)              # Convertimos a número
            dv_ingresado = dv_ingresado.upper()       # La 'k' minúscula pasa a 'K'

            # Algoritmo Módulo 11
            suma = 0
            multiplicador = 2

            # Recorremos el RUT de atrás hacia adelante multiplicando
            for digito in reversed(str(rut_cuerpo)):
                suma += int(digito) * multiplicador
                multiplicador += 1
                if multiplicador > 7:
                    multiplicador = 2

            resto = suma % 11
            dv_calculado = 11 - resto

            # Convertimos el resultado a formato dígito verificador
            if dv_calculado == 11:
                dv_calculado = '0'
            elif dv_calculado == 10:
                dv_calculado = 'K'
            else:
                dv_calculado = str(dv_calculado)

            # Comparamos lo calculado con lo que escribió el usuario
            if dv_calculado != dv_ingresado:
                raise ValidationError("RUT ingresado no es válido (Dígito verificador incorrecto).")

        except ValueError:
             raise ValidationError("Error al procesar el RUT.")

        return rut


    # VALIDACIÓN 2: El RUT (Evitar duplicados)
    def clean_rut_dobles(self):
        rut = self.cleaned_data['rut']
        
        # A. Validar en la tabla de Login (auth_user)
        # Si el usuario intenta registrarse con un RUT que ya tiene cuenta, lo frenamos.
        if User.objects.filter(username=rut).exists():
            raise ValidationError("RUT ya registrado en el sistema. Intenta iniciar sesión.")

        # B. Validar en tu tabla de Negocio (Usuario)
        # Esto previene el error de integridad de base de datos
        if Usuario.objects.filter(rut=rut).exists():
            raise ValidationError("Ya existe un cliente registrado con este RUT.")

        return rut
    # VALIDACIÓN 3: Nombre
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Regex: Permite letras a-z, acentos y ñ.
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            raise ValidationError("El nombre solo puede contener letras.")
        return nombre

    # VALIDACIÓN 4: Apellido
    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
            raise ValidationError("El apellido solo puede contener letras.")
        return apellido

    # VALIDACIÓN 5: Contraseña
    def clean_contrasena(self):
        password = self.cleaned_data['contrasena']


        if len(password) < 4:
            raise ValidationError("La contraseña debe tener al menos 4 caracteres.")

        return password
    # VALIDACIÓN 6: Teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']

        if not telefono.startswith('+'):
            raise ValidationError("El teléfono debe comenzar con el signo '+' (Ej: +569...)")

        if len(telefono) > 12:
            raise ValidationError("El teléfono no puede tener más de 12 caracteres.")

        # Opcional: Verificar que el resto sean números
        if not telefono[1:].isdigit():
            raise ValidationError("El teléfono solo puede contener números después del '+'.")

        return telefono

    # VALIDACIÓN 7: Correo Electrónico
    def clean_correo(self):
        correo = self.cleaned_data['correo']

        # Django ya valida emails básicos, pero reforzamos tu regla exacta
        # Buscamos que tenga @ y luego un punto
        if "@" not in correo or "." not in correo.split("@")[1]:
            raise ValidationError("El correo debe tener el formato algo@dominio.algo")

        return correo
