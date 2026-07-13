import openpyxl
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

        # --- CARGA MASIVA POR EXCEL ---
        if 'archivo_excel' in request.FILES:
            archivo = request.FILES['archivo_excel']
            try:
                wb = openpyxl.load_workbook(archivo)
                ws = wb.active
            except Exception:
                messages.error(request, "El archivo no es un Excel válido (.xlsx).")
                return render(request, 'registrarLibro.html', {'form': LibroForm()})

            libros_ids = Libro.objects.values_list('id_libro', flat=True)
            numeros = []
            for id_libro in libros_ids:
                try:
                    numeros.append(int(id_libro.replace("LBR", "")))
                except:
                    pass
            contador = max(numeros) + 1 if numeros else 1

            exitosos = 0
            errores = []

            for i, fila in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                if not any(fila):
                    continue
                try:
                    titulo      = str(fila[0]).strip() if fila[0] else None
                    autor       = str(fila[1]).strip() if fila[1] else None
                    editorial   = str(fila[2]).strip() if fila[2] else None
                    anio        = int(fila[3]) if fila[3] else None
                    stock       = int(fila[4]) if fila[4] else 0
                    cat_nombre  = str(fila[5]).strip() if fila[5] else None
                    descripcion = str(fila[6]).strip() if fila[6] else ''

                    if not titulo or not autor or not editorial or not anio:
                        errores.append(f"Fila {i}: faltan campos obligatorios.")
                        continue

                    categoria = None
                    if cat_nombre:
                        try:
                            categoria = Categoria.objects.get(nombre__iexact=cat_nombre)
                        except Categoria.DoesNotExist:
                            errores.append(f"Fila {i}: categoría '{cat_nombre}' no existe, libro guardado sin categoría.")

                    Libro.objects.create(
                        id_libro=f"LBR{contador}",
                        titulo=titulo,
                        autor=autor,
                        editorial=editorial,
                        anio=anio,
                        stock=stock,
                        categoria=categoria,
                        descripcion=descripcion,
                        activo=True,
                    )
                    contador += 1
                    exitosos += 1

                except Exception as e:
                    errores.append(f"Fila {i}: error — {str(e)}")

            return render(request, 'registrarLibro.html', {
                'form': LibroForm(),
                'exitosos': exitosos,
                'errores': errores,
            })

        # --- REGISTRO INDIVIDUAL ---
        else:
            form = LibroForm(request.POST)
            if form.is_valid():
                libro_nuevo = form.save(commit=False)

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

def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id=id, activo=True)
    return render(request, 'detalleLibro.html', {'libro': libro})


