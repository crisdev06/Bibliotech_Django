from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Usuario
from .forms import UsuarioForm
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
def listar_usuarios(request):
    usuarios = Usuario.objects.filter(activo=True)
    contexto = {
        'usuarios': usuarios
    }
    return render(request, 'tablaUsuarios.html', contexto)

def registrar_usuario(request):
    if request.method == 'POST':
        # Pasamos el usuario actual al form (para que sepa qué opciones mostrar)
        form = UsuarioForm(request.POST, user=request.user)

        if form.is_valid():
            # 1. Preparamos los datos del Cliente (Usuario del negocio)
            usuario_negocio = form.save(commit=False)

            # Si el usuario que registra NO es superuser, forzamos que el nuevo sea ESTUDIANTE
            # (Seguridad extra por si alguien intenta trucar el HTML)
            if not request.user.is_superuser:
                usuario_negocio.tipo = 'ESTUDIANTE'

            # 2. Capturamos datos para el Login
            rut_cliente = form.cleaned_data['rut']
            nombre_cliente = form.cleaned_data['nombre']
            password_ingresada = form.cleaned_data['password']

            try:
                # Verificamos que no exista ya ese RUT en el sistema de Login
                if not User.objects.filter(username=rut_cliente).exists():

                    # --- LÓGICA DE SUPERPODERES (PUNTO 2) ---
                    es_superuser = False
                    es_staff = False

                    # Si eligieron ADMINISTRATIVO, le damos todos los poderes
                    if usuario_negocio.tipo == 'ADMINISTRATIVO':
                        es_superuser = True
                        es_staff = True

                    # Creamos el usuario de Login con los permisos calculados
                    User.objects.create_user(
                        username=rut_cliente, 
                        password=password_ingresada,
                        first_name=nombre_cliente,
                        is_superuser=es_superuser, # ¿Es Dios del sistema?
                        is_staff=es_staff          # ¿Puede entrar al /admin?
                    )

                # 3. Guardamos finalmente al Cliente en la BD
                usuario_negocio.save()

                messages.success(request, f"Usuario registrado correctamente como {usuario_negocio.get_tipo_display()}.")
                return redirect('tabla_usuarios')

            except Exception as e:
                messages.error(request, f"Error al crear el usuario: {e}")

    else:
        # GET: Mostrar formulario vacío (pasando el usuario para el filtro de opciones)
        form = UsuarioForm(user=request.user)

    return render(request, 'registrarCliente.html', {'form': form})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('tabla_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'registrarCliente.html', {'form': form})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.activo = False
    usuario.save()
    return redirect('tabla_usuarios')
