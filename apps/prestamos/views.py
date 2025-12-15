from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from .models import Prestamo
from .forms import PrestamoForm
from apps.usuarios.models import Usuario
from apps.prestamos.forms import PrestamoSolicitudForm
from django.contrib import messages

# Create your views here.
def listar_prestamos(request):
    # Aquí iría la lógica para obtener los préstamos desde la base de datos
    prestamos = Prestamo.objects.filter(activo=True) # Reemplazar con la consulta real a la base de datos
    contexto = {'prestamos': prestamos}
    return render(request, 'tablaPrestamos.html', contexto)


def registrar_prestamo(request):
    # 1. DECIDIMOS QUÉ FORMULARIO USAR
    if request.user.is_superuser:
        # Si es Admin, usa el formulario COMPLETO (puede elegir cualquier usuario)
        FormularioClase = PrestamoForm
    else:
        # Si es Alumno/Profe, usa el formulario CORTO (solo libro y fecha)
        FormularioClase = PrestamoSolicitudForm

    if request.method == 'POST':
        form = FormularioClase(request.POST)
        
        if form.is_valid():
            # "commit=False" crea el objeto en memoria pero no lo guarda en la BD todavía
            prestamo = form.save(commit=False)
            
            # 2. AUTO-ASIGNACIÓN (Solo para no-admins)
            if not request.user.is_superuser:
                try:
                    # Buscamos en la tabla de Clientes (Usuario) el perfil que coincida 
                    # con el RUT del usuario logueado.
                    # ASUMIMOS: Que el 'username' del login es el RUT del cliente.
                    usuario_real = Usuario.objects.get(rut=request.user.username)
                    
                    prestamo.usuario = usuario_real # Asignamos el usuario automáticamente
                    
                except Usuario.DoesNotExist:
                    # Si el usuario logueado no existe en la tabla de Clientes
                    messages.error(request, "Error: Tu usuario no tiene un perfil de Cliente asociado. Contacta al administrador.")
                    return render(request, 'renta.html', {'form': form})
            
            # 3. GUARDAMOS (Ahora sí va a la base de datos y descuenta stock)
            prestamo.save()
            return redirect('tabla_prestamos')
    else:
        form = FormularioClase()

    return render(request, 'renta.html', {'form': form})

def editar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('tabla_prestamos')
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'renta.html', {'form': form})

def eliminar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    prestamo.activo = False
    prestamo.save()
    return redirect('tabla_prestamos')

def devolucion_libro(request, id_prestamo):
    prestamo = get_object_or_404(Prestamo, id=id_prestamo)
    
    if not prestamo.fecha_devolucion_real:
        prestamo.fecha_devolucion_real = date.today()
        prestamo.libro.stock += 1
        prestamo.libro.save()
        prestamo.save()
        
    return redirect('tabla_prestamos')