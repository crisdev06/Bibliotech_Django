from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import LibroForm
from .models import Libro, Categoria
from django.contrib import messages



def listar_libros(request):
    # 1. Vamos a la base de datos y traemos TODOS los libros
    libros = Libro.objects.filter(activo=True)
    
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
            libro_nuevo = form.save(commit=False)

            # Obtenemos el número más alto existente y sumamos 1
            libros_ids = Libro.objects.values_list('id_libro', flat=True)
            numeros = []
            for id_libro in libros_ids:
                try:
                    numeros.append(int(id_libro.replace("LBR", "")))
                except:
                    pass

            nuevo_numero = max(numeros) + 1 if numeros else 1
            libro_nuevo.id_libro = f"LBR{nuevo_numero}"
            libro_nuevo.activo = True
            libro_nuevo.save()

            messages.success(request, f"Libro registrado exitosamente con código LBR{nuevo_numero}.")
            return redirect('tabla_libros')
    else:
        form = LibroForm()

    return render(request, 'registrarLibro.html', {'form': form})

"""
def registrar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            # 1. Detenemos el guardado automático para asignar el ID manualmente
            libro_nuevo = form.save(commit=False)

            # --- LÓGICA AUTO-INCREMENTAL "LBR" ---
            # Buscamos el último libro registrado en la base de datos
            ultimo_libro = Libro.objects.last() # Obtiene el último según su ID interno (PK)

            if not ultimo_libro:
                # Si no hay libros, este es el primero
                nuevo_id = "LBR1"
            else:
                # Obtenemos el ID del último (Ej: "LBR15")
                string_id = ultimo_libro.id_libro

                try:
                    # Quitamos "LBR" y convertimos a número (Ej: 15)
                    parte_numerica = int(string_id.replace("LBR", ""))
                    # Sumamos 1 y volvemos a armar el string
                    nuevo_id = f"LBR{parte_numerica + 1}"
                except:
                    # Si el último ID tenía un formato raro, reiniciamos o usamos fallback
                    nuevo_id = "LBR1"

            # Asignamos el ID generado al objeto
            libro_nuevo.id_libro = nuevo_id
            libro_nuevo.activo = True

            # Guardamos definitivamente
            libro_nuevo.save()

            messages.success(request, f"Libro registrado exitosamente con código {nuevo_id}.")
            return redirect('tabla_libros')
    else:
        form = LibroForm()

    return render(request, 'registrarLibro.html', {'form': form})
"""


def editar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro) # Cargamos los datos existentes
        if form.is_valid():
            form.save()
            return redirect('tabla_libros')
    else:
        form = LibroForm(instance=libro) # Formulario precargado
    
    return render(request, 'registrarLibro.html', {'form': form}) # Reusamos el template


def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    libro.activo = False # Apagamos el interruptor
    libro.save()
    return redirect('tabla_libros')

def catalogo(request):
    query = request.GET.get('search', '')
    categorias_sel = request.GET.getlist('categoria') 
    autores_sel = request.GET.getlist('autor')
    editoriales_sel = request.GET.getlist('editorial')
    anios_sel = request.GET.getlist('anio')

    libros = Libro.objects.filter(activo=True)

    if query:
        libros = libros.filter(titulo__icontains=query) | libros.filter(autor__icontains=query)
    if categorias_sel:
        libros = libros.filter(categoria__id__in=categorias_sel)
    if autores_sel:
        libros = libros.filter(autor__in=autores_sel)
    if editoriales_sel:
        libros = libros.filter(editorial__in=editoriales_sel)
    if anios_sel:
        libros = libros.filter(anio__in=anios_sel)

    # Datos para los filtros del sidebar (solo de libros activos)
    todos_libros = Libro.objects.filter(activo=True)

    return render(request, 'catalogo.html', {
        'libros': libros,
        'categorias': Categoria.objects.all(),
        'autores': todos_libros.values_list('autor', flat=True).distinct().order_by('autor'),
        'editoriales': todos_libros.values_list('editorial', flat=True).distinct().order_by('editorial'),
        'anios': todos_libros.values_list('anio', flat=True).distinct().order_by('-anio'),
        # Selecciones actuales para mantener los checks al recargar
        'categorias_sel': categorias_sel,
        'autores_sel': autores_sel,
        'editoriales_sel': editoriales_sel,
        'anios_sel': anios_sel,
    })

"""
def catalogo(request):

    query = request.GET.get('search', '')
    
    if query:
        # Filtra si hay texto en el buscador
        libros = Libro.objects.filter(activo=True, titulo__icontains=query)
    else:
        # Trae todo si el buscador está vacío
        libros = Libro.objects.filter(activo=True)
        
    context = {
        'libros': libros
    }
    
    return render(request, 'catalogo.html', context)
"""