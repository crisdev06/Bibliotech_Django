from django.shortcuts import render

# Create your views here.
def listar_prestamos(request):
    # Aquí iría la lógica para obtener los préstamos desde la base de datos
    prestamos = []  # Reemplazar con la consulta real a la base de datos

    return render(request, 'prestamos/lista_prestamos.html', {'prestamos': prestamos})