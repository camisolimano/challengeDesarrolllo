from django.db import models

class Alumno(models.Model):
    nombre=models.CharField( max_length=50)
    apellido=models.CharField( max_length=50)
    fecha_nac=models.DateField()
    dni=models.CharField(max_length=20, unique=True)
    direccion=models.CharField(max_length=30)

class Sede(models.Model):
    nombre=models.CharField()
    direccion=models.CharField()
    ciudad=models.CharField()
    telefono=models.CharField()
    cant_aulas=models.IntegerField()

class Curso(models.Model):
    codigo_curso=models.IntegerField(primary_key=True)
    año_dictado=models.IntegerField()
    duracion=models.IntegerField()
    tema=models.CharField()
    costo_mensual=models.DecimalField(max_digits=20, decimal_places=3)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    sede= models.ForeignKey(Sede, on_delete=models.CASCADE)#un curso se dicta en una sede, pero en una sede hay muchos cursos
    alumnos=models.ManyToManyField(Alumno)