from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from Invitado.forms import InvitadoForm
from Invitado.models import Invitado
from Comite.forms import CorreoForm
from Invitado.forms import PersonaInvitadoForm
from Persona.models import Persona
from Persona.forms import PersonaForm

def indice(request):
    invitado = Invitado.objects.all()
    context = RequestContext(request, {
            'invitado'    : invitado,
    })
    return render(request, 'Invitado/index.html', context)

#
#Vista encargada de mostrar los detalles de las personas invitadas
#
def detalle(request, invitado_correo):
    persona = get_object_or_404(Persona,pk=invitado_correo)
    invitado = get_object_or_404(Invitado,correo=invitado_correo)
    
    return render(request, 'Invitado/detalle.html', {'invitado':invitado, 'persona':persona})


def mostrarFormComprobar(request):
    form = CorreoForm()
    return render(request, 'Invitado/comprobarEmailInvitado.html', {'form':form})

def comprobarEmailInvitado(request):
    form = ''
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            correoForm = form.cleaned_data['correo']
            try:
                per = Persona.objects.get(correo=correoForm)
            except Persona.DoesNotExist:
                per = None 
                
            if per == None:
                formPersonaInvitado = PersonaInvitadoForm(initial={'correo': correoForm})
            else:
                try:
                    inv = Invitado.objects.get(correo = correoForm)
                except Invitado.DoesNotExist:
                    inv = None
                if inv:
                    form = CorreoForm()
                    return render(request, 'Invitado/comprobarEmailInvitado.html', 
                  {'form':form, 
                   'error_message' : "El email que introdujo ya esta siendo utilizado para otro invitado"})
                else:
                    formPersonaInvitado = PersonaInvitadoForm(initial={'nombre': per.nombre, 'apellido': per.apellido,'correo': correoForm, 'dirpostal': per.dirpostal, 'institucion':per.institucion, 'telefono': per.telefono, 'pais': per.pais, 'pagina': per.pagina})

            return render(request, 'Invitado/crearInvitado.html', {'formPersonaInvitado':formPersonaInvitado,})
        else:
            form = CorreoForm()
    return render(request, 'Invitado/comprobarEmailInvitado.html', 
                  {'form':form, 
                   'error_message' : "Coloque un email valido."})

def crearInvitado(request):
    form = ''
    def armarEntidad(persona, invitado):

        persona.nombre = formPersonaInvitado.cleaned_data['nombre']
        persona.apellido = formPersonaInvitado.cleaned_data['apellido']
        persona.correo = formPersonaInvitado.cleaned_data['correo']
        persona.dirpostal = formPersonaInvitado.cleaned_data['dirpostal']
        persona.institucion = formPersonaInvitado.cleaned_data['institucion']
        persona.telefono = formPersonaInvitado.cleaned_data['telefono']
        persona.pais = formPersonaInvitado.cleaned_data['pais']
        persona.pagina = formPersonaInvitado.cleaned_data['pagina']
        creado = Persona.objects.get_or_create(nombre = persona.nombre, apellido = persona.apellido, correo = persona.correo, dirpostal = persona.dirpostal, institucion = persona.institucion,
                                               telefono = persona.telefono, pais = persona.pais, pagina = persona.pagina)
        #persona.save()
        
        invitado.correo = persona
        invitado.cv = formPersonaInvitado.cleaned_data['cv']
        invitado.save()
           
    if request.method == 'POST':
        formPersonaInvitado = PersonaInvitadoForm(request.POST)
        if formPersonaInvitado.is_valid():
            persona = Persona()
            invitado = Invitado()
            armarEntidad(persona, invitado)
            return HttpResponseRedirect(reverse('Invitado:indice'))
        else:
            form = PersonaInvitadoForm()
            
    return render(request, 'Invitado/crearInvitado.html', 
                  {'formPersonaInvitado':form, 
                   'error_message' : "No se lleno el formulario correctamente. La direccion postal tiene que ser un enterooooo."})