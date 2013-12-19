from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

# Create your views here.
from Persona.models import Participante
from Persona.forms import PersonaForm

def indice(request):
    participante = Participante.objects.all()
    context = RequestContext(request, {
            'participante'    : participante,
    })
    return render(request, 'Persona/index.html', context)


def detalle(request, persona_id, persona_tipo):
    if(persona_tipo == 'participante'):
        persona = get_object_or_404(Apertura,pk=persona_id)
        return render(request, 'Persona/detalle.html', {'persona':persona, 'persona_id': persona_id})
    else:
        return HttpResponse("Error al definir una persona.")

def definirPersona(request):
    return render(request, 'Persona/definirPersona.html', {})

def mostrarFormPersona(request, persona_tipo):
    form = PersonaForm()
    return render(request, 'Persona/mostrarFormPersona.html', {'form':form,'persona_tipo':persona_tipo,})

def crear(request, persona_tipo):
    def armarEntidad(persona):
        persona.nombre = form.cleaned_data['nombre']
        persona.apellido = form.cleaned_data['apellido']
        persona.correo = form.cleaned_data['correo']
        persona.dirpostal = form.cleaned_data['dirpostal']
        persona.institucion = form.cleaned_data['institucion']
        persona.telefono = form.cleaned_data['telefono']
        persona.pais = form.cleaned_data['pais']
        persona.pagina = form.cleaned_data['pagina']
        persona.save()
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            if(persona_tipo == 'participante'):
                persona = Participante()
                armarEntidad(persona)
                return HttpResponseRedirect(reverse('Persona:indice'))
        else:
            form = PersonaForm()
            
    return render(request, 'Persona/mostrarFormPersona.html', 
                  {'form':form, 
                   'error_message' : "No se lleno el formulario correctamente. La direccion postal tiene que ser un entero.",
                   'persona_tipo':persona_tipo,})