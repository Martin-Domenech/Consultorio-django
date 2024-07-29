from django.urls import path
from pacientes.views import (
    listar_pacientes, crear_pacientes, editar_paciente, buscar_pacientes, 
    historias_clinicas_view, HistoriaClinicaCreateView, eliminar_paciente, 
    historia_clinica_editar, eliminar_historia_clinica
)
urlpatterns = [
    path("pacientes/", listar_pacientes, name="lista_pacientes"),
    path("agregar-pacientes/",  crear_pacientes, name="agregar_pacientes"),
    path('editar-pacientes/<int:paciente_id>/', editar_paciente, name='editar_pacientes'),
    path("buscar-pacientes/",  buscar_pacientes, name="buscar_pacientes"),
    path("eliminar-pacientes/<int:paciente_id>/",  eliminar_paciente, name="eliminar_pacientes"),
    path('crear_historia_clinica/<int:paciente_id>/', HistoriaClinicaCreateView.as_view(), name='crear_historiaclinica'),
    path('<int:paciente_id>/historia_clinica/', historias_clinicas_view, name='historia_clinica'),
    path('editar-historia_clinica/<int:hc_id>/', historia_clinica_editar, name='editar_historiaclinica'),
    path("eliminar-historia_clinica/<int:hc_id>/",  eliminar_historia_clinica, name="eliminar_historiaclinica"),
]