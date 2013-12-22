from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

# Create your views here.
from Persona.models import Persona
from Persona.forms import PersonaForm

def indice(request):
    persona = Persona.objects.all()
    context = RequestContext(request, {
            'persona'    : persona,
    })
    return render(request, 'Persona/index.html', context)


def mostrarFormPersona(request):
    form = PersonaForm()
    return render(request, 'Persona/mostrarFormPersona.html', {'form':form,})

def crear(request):
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
            persona = Persona()
            armarEntidad(persona)
            return HttpResponseRedirect(reverse('Persona:indice'))
            
    return render(request, 'Persona/mostrarFormPersona.html', 
                  {'form':form,})