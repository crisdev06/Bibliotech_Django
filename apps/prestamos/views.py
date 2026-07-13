import json
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.core.serializers.json import DjangoJSONEncoder
from .models import Prestamo
from .forms import PrestamoForm
from apps.usuarios.models import Usuario
from apps.libros.models import Libro
from apps.prestamos.forms import PrestamoSolicitudForm
from django.contrib import messages
from django.core.exceptions import ValidationError


def obtener_usuario_actual(request):
    try:
        return Usuario.objects.get(rut=request.user.username)
    except Usuario.DoesNotExist:
        return None


def listar_prestamos(request):
    if request.user.is_superuser:
        prestamos = Prestamo.objects.filter(activo=True)
    else:
        usuario_real = obtener_usuario_actual(request)
        if usuario_real is None:
            messages.error(request, "Error: Tu usuario no tiene un perfil de Cliente asociado.")
            prestamos = Prestamo.objects.none()
        else:
            prestamos = Prestamo.objects.filter(activo=True, usuario=usuario_real)

    for prestamo in prestamos:
        estado_correcto = 'VIGENTE'
        if prestamo.fecha_devolucion_real:
            estado_correcto = 'DEVUELTO'
        elif prestamo.fecha_devolucion < date.today():
            estado_correcto = 'ATRASADO'

        if prestamo.estado_prestamo != estado_correcto:
            Prestamo.objects.filter(pk=prestamo.pk).update(estado_prestamo=estado_correcto)
            prestamo.estado_prestamo = estado_correcto

    tiene_atrasos = any(p.estado_prestamo == 'ATRASADO' for p in prestamos)

    return render(request, 'tablaPrestamos.html', {
        'prestamos': prestamos,
        'tiene_atrasos': tiene_atrasos,
    })


def registrar_prestamo(request):
    libros_data = list(Libro.objects.filter(activo=True).values('id', 'titulo', 'autor'))

    if request.user.is_superuser:
        FormularioClase = PrestamoForm
    else:
        FormularioClase = PrestamoSolicitudForm

    if request.method == 'POST':
        form = FormularioClase(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)

            if not request.user.is_superuser:
                try:
                    usuario_real = Usuario.objects.get(rut=request.user.username)
                    prestamo.usuario = usuario_real
                except Usuario.DoesNotExist:
                    messages.error(request, "Error: Tu usuario no tiene un perfil de Cliente asociado.")
                    return render(request, 'renta.html', {'form': form, 'libros_data': libros_data})

            try:
                prestamo.save()
                messages.success(request, "Préstamo registrado exitosamente.")
                return redirect('tabla_prestamos')
            except ValidationError as e:
                messages.error(request, e.message)
                return render(request, 'renta.html', {'form': form, 'libros_data': libros_data})
    else:
        libro_id = request.GET.get('libro')
        initial = {'libro': libro_id} if libro_id else {}
        form = FormularioClase(initial=initial)

    return render(request, 'renta.html', {'form': form, 'libros_data': libros_data})


def editar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    libro_original = prestamo.libro

    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            prestamo_editado = form.save(commit=False)

            if prestamo_editado.libro != libro_original:
                libro_original.stock += 1
                libro_original.save()
                if prestamo_editado.libro.stock <= 0:
                    messages.error(request, "El libro seleccionado no tiene stock disponible.")
                    return render(request, 'renta.html', {'form': form})
                prestamo_editado.libro.stock -= 1
                prestamo_editado.libro.save()

            prestamo_editado.save()
            return redirect('tabla_prestamos')
    else:
        form = PrestamoForm(instance=prestamo)
    return render(request, 'renta.html', {'form': form})


def eliminar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)

    if not prestamo.fecha_devolucion_real:
        prestamo.libro.stock += 1
        prestamo.libro.save()

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