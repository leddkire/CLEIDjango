from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from datetime import date

# Create your views here.
from Inscripcion.models import Inscripcion
from Inscripcion.forms import InscripcionForm
from Inscripcion.forms import CorreoForm
from Inscripcion.forms import PersonaInscripcionForm
from Persona.models import Persona
from Persona.forms import PersonaForm

from funciones import getPersona
from funciones import getInscripcion

def indice(request):
    inscripcion = Inscripcion.objects.all()
    context = RequestContext(request, {
            'inscripcion'    : inscripcion,
    })
    return render(request, 'Inscripcion/index.html', context)

#
#Vista encargada de mostrar los detalles de las personas inscritas
#
def detalle(request, inscripcion_correo):
    persona = get_object_or_404(Persona,pk=inscripcion_correo)
    inscripcion = get_object_or_404(Inscripcion,correo=inscripcion_correo)   
    return render(request, 'Inscripcion/detalle.html', {'inscripcion':inscripcion, 'persona':persona})

def mostrarFormComprobar(request):
    form = CorreoForm()
    return render(request, 'Inscripcion/comprobarEmailInscripcion.html', {'form':form})

#
# Vista que se encarga del formulario para comprobar el email de la persona
# que se quiere inscribir.
#
def comprobarEmailInscripcion(request):
    form = ''
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            correoForm = form.cleaned_data['correo']
            per = getPersona(correoForm)    
            if not per:
                formPersonaInscripcion = PersonaInscripcionForm(initial={'correo': correoForm})
            else:
                ins = getInscripcion(correoForm)
                if ins:
                    form = CorreoForm()
                    return render(request, 'Inscripcion/comprobarEmailInscripcion.html', 
                  {'form':form, 
                   'error_message' : "El email que introdujo ya esta inscrito."})
                else:
                    formPersonaInscripcion = PersonaInscripcionForm(initial={'nombre': per.nombre, 'apellido': per.apellido,
                                                                   'correo': correoForm, 'dirpostal': per.dirpostal, 
                                                                   'institucion':per.institucion, 'telefono': per.telefono, 
                                                                   'pais': per.pais, 'pagina': per.pagina})
            return render(request, 'Inscripcion/crearInscripcion.html', {'formPersonaInscripcion':formPersonaInscripcion,})
        else:
            form = CorreoForm()
    return render(request, 'Inscripcion/comprobarEmailInscripcion.html', 
                  {'form':form, 
                   'error_message' : "Coloque un email valido."})
        
#
# Funcion que toma como argumento, los datos de un form de html.
# Se encarga de tomar los datos del form para crear una persona
# y crear un miembro del comite, si no existen desde antes.
#            
def armarEntidad(formPersonaInscripcion):
    persona = Persona()
    inscripcion = Inscripcion()
    #Comienzan las validaciones
    persona.correo = formPersonaInscripcion.cleaned_data['correo']
    #Se crea una persona y luego se crea la inscripcion
    persona.nombre = formPersonaInscripcion.cleaned_data['nombre']
    persona.apellido = formPersonaInscripcion.cleaned_data['apellido']
    persona.dirpostal = formPersonaInscripcion.cleaned_data['dirpostal']
    persona.institucion = formPersonaInscripcion.cleaned_data['institucion']
    persona.telefono = formPersonaInscripcion.cleaned_data['telefono']
    persona.pais = formPersonaInscripcion.cleaned_data['pais']
    persona.pagina = formPersonaInscripcion.cleaned_data['pagina']
    creado = Persona.objects.get_or_create(nombre = persona.nombre, apellido = persona.apellido, correo = persona.correo, dirpostal = persona.dirpostal, institucion = persona.institucion,
                                           telefono = persona.telefono, pais = persona.pais, pagina = persona.pagina)
    inscripcion.correo = persona
    inscripcion.fechainscripcion = date.today()
    inscripcion.fechatope = date(2014,01,31)
    if inscripcion.fechatope<inscripcion.fechainscripcion:
        inscripcion.tarifa = 200
    else:
        inscripcion.tarifa = 100
    inscripcion.save()
    return True

#
# Vista que trabaja con el form para agregar una inscripcion
#
def crearInscripcion(request):
    if request.method == 'POST':
        formPersonaInscripcion = PersonaInscripcionForm(request.POST)
        if formPersonaInscripcion.is_valid():
            if armarEntidad(formPersonaInscripcion):
                return HttpResponseRedirect(reverse('Inscripcion:indice'))
            else:
                return render(request, 'Inscripcion/crearInscripcion.html',)
        else:
            form = PersonaInscripcionForm()
            
    return render(request, 'Inscripcion/crearInscripcion.html', 
                  {'formPersonaInscripcion':form, 
                   'error_message' : "No se lleno el formulario correctamente. La direccion postal tiene que ser un entero."})