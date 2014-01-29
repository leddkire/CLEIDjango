from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# Create your views here.
from Comite.models import Comite, Moderador
from Comite.forms import ComiteForm, CorreoForm, PersonaComiteForm, ModeradorForm
from Persona.models import Persona
from Persona.forms import PersonaForm
from funciones import getPersona, getComite

def indice(request):
    comite = Comite.objects.all()
    moderadores = Moderador.objects.all()
    context = RequestContext(request, {
            'comite'    : comite,
            'moderadores':moderadores,
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

#
#Hace una consulta de las personas del comite que son presidente.(Deberia haber solo una)
#
def existePresidente():
    per = None
    try:
        per = Comite.objects.get(presidente = True)
        if per:
            return True
    except Comite.DoesNotExist:
        per = None
        return False
        
#
# Vista que se encarga del formulario para comprobar el email del miembro del comite 
# que se quiere agregar.
#
def comprobarEmailComite(request):
    form = ''
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            correoForm = form.cleaned_data['correo']
            per = getPersona(correoForm)    
            if not per:
                formPersonaComite = PersonaComiteForm(initial={'correo': correoForm})
            else:
                com = getComite(correoForm)
                if com:
                    form = CorreoForm()
                    return render(request, 'Comite/comprobarEmailComite.html', 
                  {'form':form, 
                   'error_message' : "El email que introdujo ya esta siendo utilizado para otro miembro del comite"})
                else:
                    formPersonaComite = PersonaComiteForm(initial={'nombre': per.nombre, 'apellido': per.apellido,
                                                                   'correo': correoForm, 'dirpostal': per.dirpostal, 
                                                                   'institucion':per.institucion, 'telefono': per.telefono, 
                                                                   'pais': per.pais, 'pagina': per.pagina})
                    
            return render(request, 'Comite/crearComite.html', {'formPersonaComite':formPersonaComite,})
        else:
            form = CorreoForm()
    return render(request, 'Comite/comprobarEmailComite.html', 
                  {'form':form, 
                   'error_message' : "Coloque un email valido."})

        
#
# Funcion que toma como argumento, los datos de un form de html.
# Se encarga de tomar los datos del form para crear una persona
# y crear un miembro del comite, si no existen desde antes.
#            
def armarEntidad(formPersonaComite):

        persona = Persona()
        comite = Comite()
        #Comienzan las validaciones
        persona.correo = formPersonaComite.cleaned_data['correo']
        comite.presidente = formPersonaComite.cleaned_data['presidente']
        #Si el integrante del comite que se quiere agregar es presidente, se comprueba si
        #ya existe un presidente en la conferencia(no se puede tener mas de uno).
        if comite.presidente == None:
            comite.presidente = False
        else:
            if comite.presidente == True:
                #Si existe un presidente en la base de datos, no se crea el miembro del comite
                #y se devuelve false.
                if existePresidente():
                    return False            
        #Se crea una persona y luego se crea el miembro del comite.
        persona.nombre = formPersonaComite.cleaned_data['nombre']
        persona.apellido = formPersonaComite.cleaned_data['apellido']
        persona.dirpostal = formPersonaComite.cleaned_data['dirpostal']
        persona.institucion = formPersonaComite.cleaned_data['institucion']
        persona.telefono = formPersonaComite.cleaned_data['telefono']
        persona.pais = formPersonaComite.cleaned_data['pais']
        persona.pagina = formPersonaComite.cleaned_data['pagina']
        creado = Persona.objects.get_or_create(nombre = persona.nombre, apellido = persona.apellido, correo = persona.correo, dirpostal = persona.dirpostal, institucion = persona.institucion,
                                               telefono = persona.telefono, pais = persona.pais, pagina = persona.pagina)
        comite.correo = persona
        comite.arbitro = formPersonaComite.cleaned_data['arbitro']
        if comite.arbitro == None:
            comite.arbitro = False
        comite.save()
        return True
#
# Vista que trabaja con el form para agregar un miembro al comite.
#
def crearComite(request):
           
    if request.method == 'POST':
        formPersonaComite = PersonaComiteForm(request.POST)
        if formPersonaComite.is_valid():
            if armarEntidad(formPersonaComite):
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
                   'error_message' : "No se lleno el formulario correctamente."})

def agregarMod(request):
    if request.method == 'POST':
        form = ModeradorForm(request.POST)
        if form.is_valid():
            mod = Moderador(comite = form.cleaned_data['comite'])
            mod.save()
            return HttpResponseRedirect(reverse('Comite:indice'))
        else:
            return render(request, 'Comite/agregarMod.html', {'form':form,})
    else:
        form = ModeradorForm()
        return render(request, 'Comite/agregarMod.html', {'form':form})
        