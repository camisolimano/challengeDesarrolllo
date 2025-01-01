from django import forms
from django.forms import ModelForm, ValidationError
from .models import Alumno, Curso,Sede
from django.forms import ModelForm

class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'fecha_nac','dni','direccion']
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError("El DNI debe tener exactamente 8 dígitos.")
        if Alumno.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Ya existe un alumno con este DNI.")
    
        return dni


class CursoForm(ModelForm):
    alumnos=forms.ModelMultipleChoiceField(
    queryset=Alumno.objects.all(),
    widget=forms.CheckboxSelectMultiple, 
    required=False
    )
    sede = forms.ModelChoiceField(
        queryset=Sede.objects.all(), 
        empty_label="Seleccione una sede", 
        required=True  
    )
    class Meta:
        model = Curso
        fields = ['codigo_curso','año_dictado', 'duracion', 'tema','costo_mensual','fecha_inicio','fecha_fin','alumnos','sede']
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo_curso')
        if Curso.objects.filter(codigo_curso=codigo).exists():
            raise ValidationError("Ya existe un curso con este codigo.")
    
        return codigo
    
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        año_dictado = self.cleaned_data.get('año_dictado')

        if fecha_inicio:
            if fecha_inicio.year != año_dictado:
                raise ValidationError("El año del curso debe coincidir con el año de inicio.")
        return fecha_inicio

class AltaBajaAlumnos(forms.Form):
   
    codigo_curso=forms.IntegerField(label="codigo_curso")
    dni_alumno=forms.CharField(max_length=10,label="dni")
    accion=forms.ChoiceField(choices=[('alta','Alta'),('baja','Baja')], label ="Accion")