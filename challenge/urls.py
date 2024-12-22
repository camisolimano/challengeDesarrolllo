"""
URL configuration for challenge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import RedirectView

from gestionCursos import views

urlpatterns = [
    path('', RedirectView.as_view(url='/signin/')),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('pagina_principal/', views.pagina_principal, name='pagina_principal'),
    path('crear_Alumno/', views.crear_Alumno, name='crear_Alumno'),
    path('crear_Curso/', views.crear_Curso, name='crear_Curso'),
    path('borrar_Alumno/', views.borrar_Alumno, name='borrar_Alumno'),
    path('borrar_Curso/', views.borrar_Curso, name='borrar_Curso'),
    path('listado_Alumnos/', views.listado_Alumnos, name='listado_Alumnos'),
    path('listado_Cursos/', views.listado_Cursos, name='listado_Cursos'),
    path('detalles_Alumno/', views.detalles_Alumno, name='detalles_Alumno'),
    path('listado_Sedes/', views.listado_Sedes, name='listado_Sedes'),
    path('alta_baja_cursos/', views.alta_baja_cursos, name='alta_baja_cursos'),
    path('detalle_Curso/', views.detalle_Curso, name='detalle_Curso'),
    path('detalle_Sede/', views.detalle_Sede, name='detalle_Sede'),
    path('modificar_nota/<int:alumno_id>/<int:codigo_curso>/', views.modificar_nota, name='modificar_nota'),
    path('historial_Alumno/<int:dni>/', views.historial_Alumno, name='historial_Alumno'),



]
