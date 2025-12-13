from django.shortcuts import render

# Create your views here.
def listar_usuarios(request):
    # Aquí iría la lógica para obtener los usuarios desde la base de datos
    usuarios = []  # Reemplazar con la consulta real a la base de datos

    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})