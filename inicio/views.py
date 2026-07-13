from django.shortcuts import render
from apps.libros.models import Libro
from apps.prestamos.models import Prestamo
from django.db.models import Count


# Create your views here.

def vista_index(request):
    # Traemos los 8 libros más prestados contando sus préstamos activos
    libros_destacados = Libro.objects.filter(activo=True).annotate(
        total_prestamos=Count('prestamo')
    ).order_by('-total_prestamos')[:8]

    return render(request, 'index.html', {
        'libros_destacados': libros_destacados
    })

def vista_login(request):
    # Esta vista renderiza la plantilla de login
    return render(request, 'login.html')

