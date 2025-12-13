from django.shortcuts import render, redirect
from .forms import LibroForm
from .models import Libro

def listar_libros(request):
    # 1. Vamos a la base de datos y traemos TODOS los libros
    libros = Libro.objects.filter(estado=True)
    
    # 2. Guardamos esos libros en un "contexto" (una cajita de datos)
    contexto = {
        'libros': libros
    }
    
    # 3. Le enviamos ese contexto al template HTML (que crearemos después)
    return render(request, 'tablaLibros.html', contexto)

def registrar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('tabla_libros') 
    else:
        form = LibroForm()

    contexto = {'form': form}
    return render(request, 'registrarLibro.html', contexto)
