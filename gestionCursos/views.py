from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Alumno, Curso, Sede
from .forms import AlumnoForm,CursoForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method=="GET":
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        try:
            user=User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            login(request,user)
            return redirect ('home/')
        except:
            return render(request,'signup.html',{
                'form': UserCreationForm,
                'error': 'El usuario ya existe'
            })
        
def signin(request):
     if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
     else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrecta."})
        login(request, user)
        return redirect('singin/')

def crear_Alumno(request):
    if request.method == 'GET':
        return render(request, 'crear_Alumno.html', {"form": AlumnoForm })
    else:
        alumno=AlumnoForm(request.POST)
        alumno.save()
    return redirect('alumnos/')



def borrar_Alumno(request):
    if request.method=="POST":
        dni_al=request.POST.get('dni')
        try:
            alumno = Alumno.objects.get(dni=dni_al)   
            alumno.delete()
            return render(request, 'borrar_alumno.html', {'alumno': alumno, 'dni_alumno': dni_al})
        except:
            return render(request, 'borrar_alumno.html', {'error': 'No se encontró un alumno con ese DNI.'})

    return render(request, 'borrar_alumno.html')



def crear_Curso(request):
    if request.method == 'GET':
        return render(request, 'crear_Curso.html', {"form": CursoForm })
    else:
        form=CursoForm(request.POST)
        if form.is_valid():
            curso=form.save(commit=False)
            curso.save()
            form.save_m2m()
    return redirect('crear_Curso/')

def borrar_Curso(request):
    if request.method=="POST":
        codigo_str = request.POST.get('codigo_curso')
        try:
            codigo = int(codigo_str)
            curso = Curso.objects.get(codigo_curso=codigo)   
            curso.delete()
            return render(request, 'borrar_curso.html', {'curso': curso, 'codigo': codigo})
        except:
            return render(request, 'borrar_curso.html', {'error': 'No se encontró el curso con ese codigo.'})

    return render(request, 'borrar_curso.html')

        
