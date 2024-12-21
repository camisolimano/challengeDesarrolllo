from django import forms
from django.forms import ModelForm
from .models import Alumno, Curso,Sede
from django.forms import ModelForm

class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'fecha_nac','dni','direccion']


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

