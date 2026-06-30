from django.shortcuts import render

# Create your views here.

def vista_index(request):
    # Esta vista renderiza el index.html que acabamos de modificar
    return render(request, 'index.html')

def vista_login(request):
    # Esta vista renderiza la plantilla de login
    return render(request, 'login.html')

