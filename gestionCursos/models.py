from datetime import date
from django.db import models
from django.core.validators import MinLengthValidator

class Alumno(models.Model):
    nombre=models.CharField( max_length=50)
    apellido=models.CharField( max_length=50)
    fecha_nac=models.DateField()
    dni=models.CharField(max_length=8, unique=True,validators=[MinLengthValidator(8)])
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
    sede= models.ForeignKey(Sede, on_delete=models.CASCADE)
    alumnos=models.ManyToManyField(Alumno)

    @property
    def es_activo(self):
        hoy=date.today()
        return self.fecha_inicio<= hoy <= self.fecha_fin
    
    @property
    def no_ha_empezado(self):
        hoy = date.today()
        return hoy < self.fecha_inicio
    
class Inscripcion_Curso_Alumno(models.Model):
    alumno=models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    nota=models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)

    def aprobo(self):
        return self.nota is not None and self.nota>=6