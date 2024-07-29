from django import forms
from .models import HistoriaClinica, ImagenHistoriaClinica

class PacienteFormulario(forms.Form):
    nombre = forms.CharField(required=True, max_length=50)
    apellido = forms.CharField(required=True, max_length=50)
    dni = forms.CharField(required=True, max_length=15)
    telefono = forms.CharField(required=True, max_length=50)
    fecha_nacimiento = forms.CharField(required=False, max_length=50)
    derivada_por = forms.CharField(required=False, max_length=50)

class HClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['motivo_consulta', 'comentario_consulta', 'sintomas', 'examen_fisico']
        

class ImagenHistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = ImagenHistoriaClinica
        fields = ['imagen']