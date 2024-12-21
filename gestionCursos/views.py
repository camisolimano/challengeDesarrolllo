from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Alumno, Curso, Sede
from .forms import AlumnoForm,CursoForm,AltaBajaAlumnos
from django.db.models import Q
from datetime import date, datetime
from django.contrib import messages

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
            print("Alumno encontrado:", alumno)
            if 'eliminar' in request.POST: 
                alumno.delete()
                return render(request, 'borrar_alumno.html', {'mensaje': 'Alumno borrado exitosamente'})
            return render(request, 'borrar_alumno.html', {'alumno':alumno, 'dni': dni_al})

        except Alumno.DoesNotExist:
            return render(request, 'borrar_alumno.html', {'error': 'No se encontró un alumno con ese DNI.'})
    return render(request, 'borrar_alumno.html')

def detalles_Alumno(request):
    dni=request.GET.get('dni','')
    alumno=None
    if dni:
        try:
            alumno=Alumno.objects.get(dni=dni)
        except Alumno.DoesNotExist:
            return render(request,'detalles_Alumno.html', {'error' : 'No hay ningun alumno con ese DNI'})

    return render(request,'detalles_Alumno.html', {'alumno' : alumno})


def listado_Alumnos(request):
    errores = []
    nombre_al=request.GET.get('nombre','')
    apellido_al=request.GET.get('apellido','')
    fecha_nac_al=request.GET.get('fecha_nac','')
    edad=request.GET.get('edad','')

    alumnos=Alumno.objects.all()

    if nombre_al:
        alumnos=alumnos.filter(Q(nombre=nombre_al))
        
    if apellido_al:
        alumnos=alumnos.filter(Q(apellido=apellido_al))

    if fecha_nac_al:
        try:
            fecha_nac=datetime.strptime(fecha_nac_al,'%Y-%m-%d').date()
            alumnos=alumnos.filter(fecha_nac=fecha_nac)
        except ValueError:
            errores.append("Formato de fecha inválido. Use YYYY-MM-DD")

    if edad:
       edad=int(edad)
       hoy=date.today()
       fecha_i=hoy.replace(year=hoy.year-edad)
       fecha_f=hoy.replace(year=hoy.year-edad-1)
       alumnos = alumnos.filter(fecha_nac__lte=fecha_i, fecha_nac__gt=fecha_f)
    
    for alumno in alumnos:
        alumno.edad = (date.today() - alumno.fecha_nac).days // 365

    context = {
        'alumnos': alumnos,
        'errores': errores,
    }
    return render(request,'listado_Alumnos.html', context)

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
            if 'eliminar' in request.POST:   
                curso.delete()
                return render(request, 'borrar_Curso.html', {'mensaje': 'Curso borrado exitosamente'})
            return render(request, 'borrar_Curso.html', {'curso': curso, 'codigo_curso': codigo})
        except Curso.DoesNotExist:
            return render(request, 'borrar_Curso.html', {'error': 'No se encontró el curso con ese codigo.'})
    return render(request, 'borrar_Curso.html')

def listado_Cursos(request):
    errores = []
    duracion=request.GET.get('duracion','')
    año_dictado=request.GET.get('año_dictado','')
    fecha_inicio=request.GET.get('fecha_inicio','')
    sede=request.GET.get('sede','')
    costo=request.GET.get('costo_mensual','')

    cursos=Curso.objects.all()

    if duracion:
        cursos=cursos.filter(duracion=duracion)
        
    if año_dictado:
        cursos=cursos.filter(año_dictado=año_dictado)

    if fecha_inicio:
        try:
            fecha_ini=datetime.strptime(fecha_inicio,'%Y-%m-%d').date()
            cursos=cursos.filter(fecha_inicio=fecha_ini)
        except ValueError:
            errores.append("Formato de fecha inválido. Use YYYY-MM-DD")

    if sede:
       cursos = cursos.filter(sede__nombre__icontains=sede)
  
    if costo:
       cursos = cursos.filter(costo_mensual=costo)
  
    context = {
        'cursos': cursos,
        'errores': errores,
    }
    return render(request,'listado_Cursos.html', context)




def listado_Sedes(request):
    errores = []
    ciudad=request.GET.get('ciudad','').strip()
    nombre=request.GET.get('nombre','').strip()

 
    sedes=Sede.objects.all()

    if nombre:
        sedes=sedes.filter(nombre__icontains=nombre)
        
    if ciudad:
        sedes=sedes.filter(ciudad__icontains=ciudad)
 
    return render(request,'listado_Sedes.html', { 'sedes': sedes,
})


def alta_baja_cursos(request):
    if request.method=="POST":
       form=AltaBajaAlumnos(request.POST)
       if form.is_valid():
            cod_curso=form.cleaned_data['codigo_curso']
            dni_al=form.cleaned_data['dni_alumno']          
            accion=form.cleaned_data['accion']

            try:
               alumno=Alumno.objects.get(dni=dni_al)               
               curso=Curso.objects.get(codigo_curso=cod_curso)

               if accion == 'alta':
                   curso.alumnos.add(alumno)
                   messages.success(request, f"Alumno {alumno.nombre} {alumno.apellido} agregado al curso.")
               elif accion == 'baja':
                    curso.alumnos.remove(alumno)
                    messages.success(request, f"Alumno {alumno.nombre} {alumno.apellido} eliminado del curso.")
            except Alumno.DoesNotExist:
                messages.error(request, "El alumno con ese dni no existe.")
            except Curso.DoesNotExist:
                messages.error(request, "El curso con ese código no existe.")
            return redirect('alta_baja_cursos')
    else:
        form=AltaBajaAlumnos(request.POST)

    return render(request,'alta_baja_cursos.html',{'form': form })

