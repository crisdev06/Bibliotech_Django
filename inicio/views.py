from django.shortcuts import render

# Create your views here.

def vista_index(request):
    # Esta vista renderiza el index.html que acabamos de modificar
    return render(request, 'index.html')

def vista_registrar_cliente(request):
    # Esta vista renderiza la plantilla para registrar clientes
    return render(request, 'registrarCliente.html')

def vista_registrar_libro(request):
    # Esta vista renderiza la plantilla para registrar libros
    return render(request, 'registrarLibro.html')

def vista_renta(request):
    # Esta vista renderiza la plantilla para la renta de libros
    return render(request, 'renta.html')

def vista_login(request):
    # Esta vista renderiza la plantilla de login
    return render(request, 'login.html')