from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Paciente(models.Model):
    nombre = models.CharField(max_length=50, blank=False)
    apellido = models.CharField(max_length=50, blank=False)
    dni = models.CharField(max_length=15, blank=False)
    telefono = models.CharField(max_length=50, blank=False, null=True)
    fecha_nacimiento = models.CharField(max_length=50, blank=True, null=True)
    derivada_por = models.CharField(max_length=50, blank=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
class HistoriaClinica(models.Model):
    motivo_consulta = models.CharField(max_length=256, blank=True)
    comentario_consulta = models.TextField()
    sintomas = models.CharField(max_length=256, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    examen_fisico = models.CharField(max_length=256, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class ImagenHistoriaClinica(models.Model):
    imagen = models.ImageField(upload_to='img_hc', null=True, blank=True)
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE)