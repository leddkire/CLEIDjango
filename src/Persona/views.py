from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from Persona.models import Persona
from Persona.forms import PersonaForm
from Persona.funciones import guardarPersona
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

    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = Persona()
            guardarPersona(persona,form)
            return HttpResponseRedirect(reverse('Persona:indice'))
            
    return render(request, 'Persona/mostrarFormPersona.html', 
                  {'form':form,})