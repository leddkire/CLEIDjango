from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# Create your views here.
from Conferencia.models import Conferencia
from Conferencia.forms import ConferenciaForm

def indice(request):
    conferencia = Conferencia.objects.all()
    context = RequestContext(request, {
            'conferencia'    : conferencia,
    })
    return render(request, 'Conferencia/index.html', context)

#
#Procedmiento que se encarga de realizar la consulta de conferencia a la bas de datos, devuelve el resultado.
#
def conferenciaVacio():
    try:
        confe = Conferencia.objects.all()
    except Conferencia.DoesNotExist:
        confe = None
    return confe

#
#Vista que se encargara de mostar el formulario de editar datos de conferencia.
#Si la conferencia ya tiene datos, se muestran al inicio.
#
def mostrarFormConferencia(request):
    confe = conferenciaVacio()
    if confe:
        formConferencia = ConferenciaForm(initial={'anio': confe[0].anio, 'duracion': confe[0].duracion, 'pais':confe[0].pais, 
                                                   'maxArticulos':confe[0].maxArticulos})
    else:
        formConferencia = ConferenciaForm()
    return render(request, 'Conferencia/editarDatosConferencia.html', {'formConferencia':formConferencia, })

def editarDatosConferencia(request):
    
    def armarEntidad(conferencia):

        conferencia.anio = formConferencia.cleaned_data['anio']
        conferencia.duracion = formConferencia.cleaned_data['duracion']
        conferencia.pais = formConferencia.cleaned_data['pais']
        conferencia.maxArticulos = formConferencia.cleaned_data['maxArticulos']
        
        try:
            confe = Conferencia.objects.get(anio = conferencia.anio)
        except Conferencia.DoesNotExist:
            confe = None

        if confe:
            confe.anio = conferencia.anio
            confe.duracion = conferencia.duracion
            confe.pais = conferencia.pais
            confe.maxArticulos = conferencia.maxArticulos
            confe.save()
        else:
            existe = Conferencia.objects.all()
            if not existe:
                conferencia.save()   
        #conf, creado = Conferencia.objects.get_or_create(anio = conferencia.anio, duracion = conferencia.duracion,
         #                                          pais = conferencia.pais, maxArticulos = conferencia.maxArticulos)
                   
    
    formConferencia = ''
    if request.method == 'POST':
        formConferencia = ConferenciaForm(request.POST)
        if formConferencia.is_valid():
            conferencia = Conferencia()
            armarEntidad(conferencia)
            return HttpResponseRedirect(reverse('Conferencia:indice'))
        else:
            form = ConferenciaForm()
            
    return render(request, 'Conferencia/editarDatosConferencia.html', 
                  {'formConferencia':form, 
                   'error_message' : "No se lleno el formulario correctamente."})
