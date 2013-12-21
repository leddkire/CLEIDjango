from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# Create your views here.
from Comite.models import Comite
from Comite.forms import ComiteForm
from Comite.forms import CorreoForm
from Comite.forms import PersonaComiteForm
from Persona.models import Persona
from Persona.forms import PersonaForm

def indice(request):
    comite = Comite.objects.all()
    context = RequestContext(request, {
            'comite'    : comite,
    })
    return render(request, 'Comite/index.html', context)
#
#Vista encargada de mostrar los detalles de las personas dal comite
#
def detalle(request, comite_correo):
    persona = get_object_or_404(Persona,pk=comite_correo)
    comite = get_object_or_404(Comite,correo=comite_correo)
    
    return render(request, 'Comite/detalle.html', {'comite':comite, 'persona':persona})

def mostrarFormComprobar(request):
    form = CorreoForm()
    return render(request, 'Comite/comprobarEmailComite.html', {'form':form})

def comprobarEmailComite(request):
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
                formPersonaComite = PersonaComiteForm(initial={'correo': correoForm})
            else:
                try:
                    com = Comite.objects.get(correo = correoForm)
                except Comite.DoesNotExist:
                    com = None
                if com:
                    form = CorreoForm()
                    return render(request, 'Comite/comprobarEmailComite.html', 
                  {'form':form, 
                   'error_message' : "El email que introdujo ya esta siendo utilizado para otro miembro del comite"})
                else:
                    formPersonaComite = PersonaComiteForm(initial={'nombre': per.nombre, 'apellido': per.apellido,'correo': correoForm, 'dirpostal': per.dirpostal, 'institucion':per.institucion, 'telefono': per.telefono, 'pais': per.pais, 'pagina': per.pagina})

            return render(request, 'Comite/crearComite.html', {'formPersonaComite':formPersonaComite,})
        else:
            form = CorreoForm()
    return render(request, 'Comite/comprobarEmailComite.html', 
                  {'form':form, 
                   'error_message' : "Coloque un email valido."})
            


def crearComite(request):
    form = ''
    def armarEntidad(persona, comite):
        
        persona.correo = formPersonaComite.cleaned_data['correo']
        comite.presidente = formPersonaComite.cleaned_data['presidente']
        
        if comite.presidente == None:
            comite.presidente = False
        else:
            if comite.presidente == True:
                per = None
                try:
                    per = Comite.objects.get(presidente = True)
                    if per:
                        return False
                except Comite.DoesNotExist:
                    per = None
            


        persona.nombre = formPersonaComite.cleaned_data['nombre']
        persona.apellido = formPersonaComite.cleaned_data['apellido']
        
        persona.dirpostal = formPersonaComite.cleaned_data['dirpostal']
        persona.institucion = formPersonaComite.cleaned_data['institucion']
        persona.telefono = formPersonaComite.cleaned_data['telefono']
        persona.pais = formPersonaComite.cleaned_data['pais']
        persona.pagina = formPersonaComite.cleaned_data['pagina']
        creado = Persona.objects.get_or_create(nombre = persona.nombre, apellido = persona.apellido, correo = persona.correo, dirpostal = persona.dirpostal, institucion = persona.institucion,
                                               telefono = persona.telefono, pais = persona.pais, pagina = persona.pagina)
        #persona.save()
        
        comite.correo = persona

        comite.arbitro = formPersonaComite.cleaned_data['arbitro']
        if comite.arbitro == None:
            comite.arbitro = False
        comite.save()
        return True
           
    if request.method == 'POST':
        formPersonaComite = PersonaComiteForm(request.POST)
        if formPersonaComite.is_valid():
            persona = Persona()
            comite = Comite()
            if armarEntidad(persona, comite):
                return HttpResponseRedirect(reverse('Comite:indice'))
            else:
                formPersonaComite.cleaned_data['presidente'] = False
                return render(request, 'Comite/crearComite.html', 
                  {'formPersonaComite':formPersonaComite, 
                   'error_message' : "Ya existe un presidente del comite."})
        else:
            form = PersonaComiteForm()
            
    return render(request, 'Comite/crearComite.html', 
                  {'formPersonaComite':form, 
                   'error_message' : "No se lleno el formulario correctamente. La direccion postal tiene que ser un enterooooo."})