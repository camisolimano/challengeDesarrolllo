from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Alumno, Curso, Sede,Inscripcion_Curso_Alumno
from .forms import AlumnoForm,CursoForm,AltaBajaAlumnos
from django.db.models import Q,Avg
from datetime import date, datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def pagina_principal(request):
    return render(request, 'pagina_principal.html')

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
        return redirect('pagina_principal')

def crear_Alumno(request):
    if request.method == 'GET':
        return render(request, 'crear_Alumno.html', {"form": AlumnoForm })
    else:
        alumno=AlumnoForm(request.POST)
        if alumno.is_valid():
            alumno.save()
            messages.success(request, "El alumno se creó exitosamente.")
            return redirect('crear_Alumno')
        else:
            messages.error(request, "Hubo un error al crear el alumno.")
            return render(request, 'crear_Alumno.html', {"form": alumno})



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
    cursos=None
    inscripciones=None
    if dni:
        try:
            alumno=Alumno.objects.get(dni=dni)
            inscripciones = Inscripcion_Curso_Alumno.objects.filter(alumno=alumno).select_related('curso','curso__sede')
            cursos = [inscripcion for inscripcion in inscripciones if inscripcion.curso.es_activo]

        except Alumno.DoesNotExist:
            return render(request,'detalles_Alumno.html', {'error' : 'No hay ningun alumno con ese DNI'})

    return render(request,'detalles_Alumno.html', {'alumno' : alumno, 'cursos': cursos})

def modificar_nota(request,alumno_id, codigo_curso):
  
        alumno = None
        curso = None
        inscripcion = None
        try:
            alumno = Alumno.objects.get(id=alumno_id)
        except Alumno.DoesNotExist:
            messages.error(request, "El alumno no existe.")
            return redirect('modificar_nota.html') 
        
        try:
            curso = Curso.objects.get(codigo_curso=codigo_curso)
        except Curso.DoesNotExist:
            messages.error(request, "El curso no existe.")
            return redirect('modificar_nota.html')  
        
        try:
            inscripcion = Inscripcion_Curso_Alumno.objects.get(alumno=alumno, curso=curso)
        except Inscripcion_Curso_Alumno.DoesNotExist:
            messages.error(request, "El alumno no está inscrito en este curso.")
            return redirect('modificar_nota.html')  
        
        if request.method=="POST":
            nueva_nota=request.POST.get('nota',None)
            if nueva_nota:
                try:
                    inscripcion.nota = float(nueva_nota)
                    inscripcion.save()
                    messages.success(request, f"Nota del alumno {alumno.nombre} {alumno.apellido} modificada con éxito.")
                    return redirect('modificar_nota.html')
                except ValueError:
                    messages.error(request, "La nota ingresada no es válida.")
            else:
                messages.error(request, "Por favor ingrese una nota válida.")
        
        return render(request, 'modificar_nota.html', {'alumno': alumno, 'curso': curso, 'inscripcion': inscripcion})


def historial_Alumno(request,dni):
    try:
        alumno=Alumno.objects.get(dni=dni)
        inscripciones = Inscripcion_Curso_Alumno.objects.filter(alumno=alumno).select_related('curso','curso__sede')
    except Alumno.DoesNotExist:
        return render('historial_Alumno.html',{'error': 'No hay ningún alumno con ese DNI.'})
            
    return render(request, 'historial_Alumno.html',{'alumno': alumno, 'inscripciones': inscripciones})




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

    paginator=Paginator(alumnos,5)
    page=request.GET.get('page')

    try:
            alumnos = paginator.page(page)
    except PageNotAnInteger:
            alumnos = paginator.page(1)
    except EmptyPage:
            alumnos = paginator.page(paginator.num_pages)

    
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
  
    paginator=Paginator(cursos,5)
    page=request.GET.get('page')

    try:
            cursos = paginator.page(page)
    except PageNotAnInteger:
            cursos = paginator.page(1)
    except EmptyPage:
            cursos = paginator.page(paginator.num_pages)

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
    
    
    paginator=Paginator(sedes,5)
    page=request.GET.get('page')

    try:
            sedes = paginator.page(page)
    except PageNotAnInteger:
            sedes = paginator.page(1)
    except EmptyPage:
            sedes = paginator.page(paginator.num_pages)

   
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
                   Inscripcion_Curso_Alumno.objects.get_or_create(alumno=alumno, curso=curso)

                   messages.success(request, f"Alumno {alumno.nombre} {alumno.apellido} agregado al curso.")
               elif accion == 'baja':
                    curso.alumnos.remove(alumno)
                    Inscripcion_Curso_Alumno.objects.filter(alumno=alumno, curso=curso).delete()

                    messages.success(request, f"Alumno {alumno.nombre} {alumno.apellido} eliminado del curso.")
            except Alumno.DoesNotExist:
                messages.error(request, "El alumno con ese dni no existe.")
            except Curso.DoesNotExist:
                messages.error(request, "El curso con ese código no existe.")
            return redirect('alta_baja_cursos')
    else:
        form=AltaBajaAlumnos(request.POST)

    return render(request,'alta_baja_cursos.html',{'form': form })

def detalle_Curso(request):
    curso=None
    inscripciones=[]
    promedio_notas=None
    codigo_curso=request.GET.get('codigo_curso','').strip()
    if codigo_curso:
        try:
            curso=Curso.objects.get(codigo_curso=codigo_curso)
            inscripciones=Inscripcion_Curso_Alumno.objects.filter(curso=curso)
            promedio_notas = inscripciones.aggregate(Avg('nota'))['nota__avg'] or 0

        except Curso.DoesNotExist:
            curso=None
            alumnos=[]
            return render(request,'detalle_Curso.html', {'error': 'No se encontro el curso'})
    return render(request, 'detalle_Curso.html',{'curso': curso, 'inscripciones': inscripciones, 'promedio_notas':promedio_notas})


def detalle_Sede(request):
    sede=None
    cursos=[]
    nombre=request.GET.get('nombre','').strip()
    if nombre:
        try:
            sede=Sede.objects.get(nombre=nombre)
            cursos = Curso.objects.filter(sede=sede) 
               
        except Sede.DoesNotExist:
            sede=None
            cursos=[]
            return render(request,'detalle_Sede.html', {'error': 'No se encontro la sede'})
        
    return render(request, 'detalle_Sede.html',{'sede': sede, 'cursos': cursos})