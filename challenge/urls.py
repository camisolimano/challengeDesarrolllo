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
    path('', RedirectView.as_view(url='/signup/')),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('crear_Alumno/', views.crear_Alumno, name='crear_Alumno'),
    path('crear_Curso/', views.crear_Curso, name='crear_Curso'),
    path('borrar_Alumno/', views.borrar_Alumno, name='borrar_Alumno'),
    path('borrar_Curso/', views.borrar_Curso, name='borrar_Curso'),


]
