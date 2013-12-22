from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# Create your views here.
from Conferencia.models import Conferencia
from Conferencia.forms import ConferenciaForm
from funciones import getArticulosAceptados
from Evaluacion.models import Evaluacion
from funciones import getEvaluacionesDeArticulo
from funciones import getArticuloPorId
from funciones import getArticulosAceptables
from funciones import getDatosConferencia

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

def armarEntidad(formConferencia):
    conferencia = Conferencia()
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

def editarDatosConferencia(request):

    if request.method == 'POST':
        formConferencia = ConferenciaForm(request.POST)
        if formConferencia.is_valid():
            armarEntidad(formConferencia)
            return HttpResponseRedirect(reverse('Conferencia:indice'))
        else:
            form = ConferenciaForm()
            
    return render(request, 'Conferencia/editarDatosConferencia.html', 
                  {'formConferencia':form, 
                   'error_message' : "No se lleno el formulario correctamente."})
    
def mostrarTiposDeArticulos(request):
    articulo = getArticulosAceptados()

    context = RequestContext(request, {
            'articulo'    : articulo,
    })
    return render(request, 'Conferencia/tiposDeSeleccionar.html', context)
#
# Funcion que realiza las consultas necesarias para determinar si un articulo es aceptable.
# Devuelve todos los articulos que: tienen promedio mayor o igual a 2.00 y tienen dos evaluaciones
# o mas.
#
def setArticulosAceptables():
    listaArticulos = []
    #Se toman todos los articulos que tienen promedio mayor a 2.00
    try:
        #Article.objects.all().annotate(arbitros_count=Count('keywords__keyword'))
        evaluacion = Evaluacion.objects.filter(promedio__gt = 2)
        #Si hubo resultados, se hace una iteracion para ver si tiene minimo dos evaluaciones.
        if evaluacion:
            for ev in evaluacion:
                if ev.arbitros.all().count() >= 2:
                    artAceptable = getArticuloPorId(ev.articulo.pk)
                    if artAceptable:
                        artAceptable.aceptable = True
                        artAceptable.save()
                        listaArticulos.append(artAceptable)
    except Evaluacion.DoesNotExist:
        evaluacion = None
    return listaArticulos

def calcular_ocurrencia(promedio,lista):
        ocurrencia=0
        for element in lista:
            if getEvaluacionesDeArticulo(element.pk).promedio==promedio:
                ocurrencia+=1
        return ocurrencia
    
# Este metodo retorna una lista de los articulos que fueron aceptados por CLEI pero que se encuentran
# dentro de la lista de empatados
def get_empatados(aceptados, aceptables):
        empatados=[]+aceptables
        for element in aceptados:
            empatados.remove(element)
        return empatados

def generarAceptados(aceptables):
    # Se verifica si el maximo de articulos es mayor que la longitud de la lista de aceptables
    # si esto pasa entonces la lista de aceptables pasa a ser la lista de aceptados, sino se busca
    # cual es la nueva lista de aceptados
    maxarticulos = getDatosConferencia()
    if maxarticulos>=len(aceptables):
        return aceptables
    else:
        if maxarticulos > 0:
            aceptados=[]
            i=0
            while i<maxarticulos:
                aceptados.append(aceptables[i])
                i+=1
            # ultimo es el promedio minimo contenido en la lista de aceptados
            ultimo=aceptados[maxarticulos-1]
            # se cuenta cuantas veces aparece el promedio en la lista de aceptados
            numvecesaccept=calcular_ocurrencia(getEvaluacionesDeArticulo(ultimo.pk).promedio, aceptados)
            # se cuenta cuantas veces aparece el promedio en la lista de aceptables
            numvecesaceptables=calcular_ocurrencia(getEvaluacionesDeArticulo(ultimo.pk).promedio, aceptables)
            # si el numero de veces de aceptados es distinto del numero de veces de aceptables
            # se procede a eliminar todos los valores que fueron admitidos en la lista de aceptados
            if numvecesaccept!=numvecesaceptables:
                while numvecesaccept>0:
                    aceptados.remove(ultimo)
                    numvecesaccept-=1
        else:
            return []
    return aceptados
      
def aceptablesNota(request):
    listaAceptables = setArticulosAceptables()
    listaAceptables = sorted(listaAceptables,key= lambda element: getEvaluacionesDeArticulo(element.pk).promedio, reverse = True)
    #articulosAceptables = getArticulosAceptables()
    articulosAceptados = generarAceptados(listaAceptables)
    articuloEmpatado = get_empatados(articulosAceptados, listaAceptables)
    #setArticulosAceptados(articulosAceptables)
    context = RequestContext(request, {
            'articuloAceptable'    : listaAceptables,
            'articuloAceptado'     : articulosAceptados,
            'articuloEmpatado'     : articuloEmpatado,
    })
    return render(request, 'Conferencia/aceptables.html', context)

