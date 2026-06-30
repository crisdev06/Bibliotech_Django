"""
URL configuration for bibliotech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from inicio import views
from apps.libros import views as libroV
from apps.usuarios import views as usuarioV
from apps.prestamos import views as prestamoV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.vista_index, name='index'),


    # Rutas de ACCESO y SALIDA
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Rutas para LIBROS
    path('registrar-libro/', libroV.registrar_libro, name='registrar_libro'),
    path('editar-libro/<int:id>/', libroV.editar_libro, name='editar_libro'),
    path('eliminar-libro/<int:id>/', libroV.eliminar_libro, name='eliminar_libro'),
    path('tabla-libros/', libroV.listar_libros, name='tabla_libros'),
    path('catalogo/', libroV.catalogo, name='catalogo'),


    # Rutas para USUARIOS
    path('registrar-cliente/', usuarioV.registrar_usuario, name='registrar_cliente'),
    path('editar-usuario/<int:id>/', usuarioV.editar_usuario, name='editar_usuario'),
    path('eliminar-usuario/<int:id>/', usuarioV.eliminar_usuario, name='eliminar_usuario'),
    path('tabla-usuarios/', usuarioV.listar_usuarios, name='tabla_usuarios'),

    # Rutas para PRESTAMOS
    path('renta/', prestamoV.registrar_prestamo, name='renta'),
    path('editar-prestamo/<int:id>/', prestamoV.editar_prestamo, name='editar_prestamo'),
    path('eliminar-prestamo/<int:id>/', prestamoV.eliminar_prestamo, name='eliminar_prestamo'),
    path('tabla-prestamos/', prestamoV.listar_prestamos, name='tabla_prestamos'),
    path('devolucion/<int:id_prestamo>/', prestamoV.devolucion_libro, name='devolucion_libro'),
]
