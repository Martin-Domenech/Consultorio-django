from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from pacientes.models import Paciente, HistoriaClinica, ImagenHistoriaClinica
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from pacientes.forms import PacienteFormulario, HClinicaForm, ImagenHistoriaClinicaForm
from django.forms import modelformset_factory

class LoginRequiredMixin(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def listar_pacientes(request):
    contexto = {
        "pacientes": Paciente.objects.all(),
    }
    http_response = render(
        request = request,
        template_name = 'pacientes/lista_pacientes.html',
        context=contexto,
    )
    return http_response

@login_required
def crear_pacientes(request):
    if request.method == "POST":
        formulario = PacienteFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data
            nombre = data["nombre"]
            apellido = data["apellido"]
            telefono = data["telefono"]
            fecha_nacimiento = data["fecha_nacimiento"]
            dni = data["dni"]

            paciente = Paciente(nombre=nombre, apellido=apellido, telefono=telefono, fecha_nacimiento=fecha_nacimiento, dni=dni, creador=request.user)
            paciente.save()

            url_exitosa = reverse('lista_pacientes')
            return redirect(url_exitosa)
    else:
        formulario=PacienteFormulario()
        
    http_response = render(
        request=request,
        template_name='pacientes/agregar_pacientes.html',
        context={'formulario': formulario}
    )
    return http_response

@login_required
def editar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    if request.method == "POST":
        formulario = PacienteFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data
            paciente.nombre = data["nombre"]
            paciente.apellido = data["apellido"]
            paciente.telefono = data["telefono"]
            paciente.fecha_nacimiento = data["fecha_nacimiento"]
            paciente.derivada_por = data["derivada_por"]
            paciente.dni = data["dni"]
            paciente.save()
            url_exitosa = reverse('historia_clinica', kwargs={'paciente_id': paciente_id})
            return redirect(url_exitosa)
    else:  # GET
        inicial = {
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            "telefono" : paciente.telefono,
            "fecha_nacimiento" : paciente.fecha_nacimiento,
            "derivada_por": paciente.derivada_por,
            "dni": paciente.dni,
        }
        formulario = PacienteFormulario(initial=inicial)
    return render(
        request=request,
        template_name='pacientes/agregar_pacientes.html',
        context={'formulario': formulario},
    )



@login_required
def buscar_pacientes(request):
    if request.method == "POST":
        data = request.POST
        busqueda = data["busqueda"]
        pacientes = Paciente.objects.filter(
            Q(nombre__contains=busqueda) | Q(apellido__contains=busqueda) | Q(dni__contains=busqueda)
        )
        contexto = {
            "pacientes": pacientes,
        }
    http_response = render(
        request=request,
        template_name='pacientes/lista_pacientes.html',
        context=contexto,
    )
    return http_response  

@login_required
def eliminar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    if request.method == "POST":
        paciente.delete()
        url_exitosa = reverse('lista_pacientes')
        return redirect(url_exitosa)


@login_required
def historias_clinicas_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    historias_clinicas = HistoriaClinica.objects.filter(paciente=paciente).order_by('-fecha')

    return render(request, 'pacientes/lista_historiaclinica.html', {'paciente': paciente, 'historias_clinicas': historias_clinicas})



# class HistoriaClinicaCreateView(LoginRequiredMixin, CreateView):
#     model = HistoriaClinica
#     form_class = HClinicaForm
#     template_name = 'pacientes/crear_historiaclinica.html'  # Reemplaza con la ruta de tu template

#     def get_initial(self):
#         # Obtén el paciente_id del argumento en la URL y configúralo como valor inicial
#         paciente_id = self.kwargs.get('paciente_id')
#         return {'paciente': paciente_id}

#     def form_valid(self, form):
#         # Configura el paciente antes de guardar la historia clínica
#         paciente_id = self.kwargs.get('paciente_id')
#         form.instance.paciente_id = paciente_id
#         return super().form_valid(form)

#     def get_success_url(self):
#         # Redirige a la página de detalles del paciente después de crear la historia clínica
#         paciente_id = self.kwargs.get('paciente_id')
#         return reverse_lazy('historia_clinica', kwargs={'paciente_id': paciente_id})



class HistoriaClinicaCreateView(LoginRequiredMixin, CreateView):
    model = HistoriaClinica
    fields = ['motivo_consulta', 'comentario_consulta', 'sintomas', 'examen_fisico']
    template_name = 'pacientes/crear_historiaclinica.html'

    def get_initial(self):
        paciente_id = self.kwargs.get('paciente_id')
        return {'paciente': paciente_id}

    def form_valid(self, form):
        paciente_id = self.kwargs.get('paciente_id')
        form.instance.paciente_id = paciente_id
        historia_clinica = form.save()

        ImagenFormSet = modelformset_factory(ImagenHistoriaClinica, form=ImagenHistoriaClinicaForm, extra=1)
        formset = ImagenFormSet(self.request.POST, self.request.FILES, queryset=ImagenHistoriaClinica.objects.none())

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    imagen = form.cleaned_data['imagen']
                    ImagenHistoriaClinica.objects.create(imagen=imagen, historia_clinica=historia_clinica)
            return redirect(reverse('historia_clinica', kwargs={'paciente_id': paciente_id}))  
        else:
            historia_clinica.delete()
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ImagenFormSet = modelformset_factory(ImagenHistoriaClinica, form=ImagenHistoriaClinicaForm, extra=1)
        if self.request.POST:
            context['formset'] = ImagenFormSet(self.request.POST, self.request.FILES, queryset=ImagenHistoriaClinica.objects.none())
        else:
            context['formset'] = ImagenFormSet(queryset=ImagenHistoriaClinica.objects.none())
        return context

    def get_success_url(self):
        paciente_id = self.kwargs.get('paciente_id')
        return reverse_lazy('historia_clinica', kwargs={'paciente_id': paciente_id})


@login_required
def historia_clinica_editar(request, hc_id):
    historia_clinica = HistoriaClinica.objects.get(id=hc_id)
    
    if request.method == 'POST':
        form = HClinicaForm(request.POST, instance=historia_clinica)
        if form.is_valid():
            form.save()
            paciente_id = historia_clinica.paciente_id
            return redirect(reverse_lazy('historia_clinica', kwargs={'paciente_id': paciente_id}))
    else:
        form = HClinicaForm(instance=historia_clinica)
    
    return render(request, 'pacientes/crear_historiaclinica.html', {'form': form})

@login_required
def eliminar_historia_clinica(request, hc_id):
    # Obtener la instancia de la historia clínica o devolver un error 404 si no existe
    historiaclinica = get_object_or_404(HistoriaClinica, id=hc_id)
    historia_clinica = HistoriaClinica.objects.get(id=hc_id)

    if request.method == "POST":
        # Confirmar que se está utilizando el método POST antes de eliminar la historia clínica
        historiaclinica.delete()
        # Después de eliminar, redirigir a una URL exitosa
        paciente_id = historia_clinica.paciente_id
        url_exitosa = url_exitosa = reverse('historia_clinica', kwargs={'paciente_id': paciente_id})
        return redirect(url_exitosa)
    