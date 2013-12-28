from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# Create your views here.
from Conferencia.models import Conferencia
from Conferencia.forms import ConferenciaForm
from Comite.forms import CorreoForm
from funciones import getArticulosAceptados
from Evaluacion.models import Evaluacion
from funciones import getEvaluacionesDeArticulo
from funciones import getArticuloPorId
from funciones import getArticulosAceptables
from funciones import getDatosConferencia
from funciones import getArticulosEmpatados
from funciones import getPersona
from funciones import getComite

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
        if len(confe) == 0:
            confe = None
    except Conferencia.DoesNotExist:
        confe = None
    return confe

#
#Vista que se encargara de mostar el formulario de editar datos de conferencia.
#Si la conferencia ya tiene datos, se muestran al inicio.
#
def mostrarFormConferencia(request):
    confe = conferenciaVacio()
    if confe != None:
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

    if confe != None:
        confe.anio = conferencia.anio
        confe.duracion = conferencia.duracion
        confe.pais = conferencia.pais
        confe.maxArticulos = conferencia.maxArticulos
        confe.save()
    else:
        existe = Conferencia.objects.all()
        if existe == None or len(existe) == 0:
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
    articulosAceptados = getArticulosAceptados()
    articulosEmpatados = getArticulosEmpatados()
    context = RequestContext(request, {
            'articulosAceptados'    : articulosAceptados,
            'articulosEmpatados'    : articulosEmpatados,
    })
    return render(request, 'Conferencia/tiposDeSeleccionar.html', context)
#
# Funcion que realiza las consultas necesarias para determinar si un articulo es aceptable.
# Devuelve todos los articulos que: tienen promedio mayor o igual a 2.00 y tienen dos evaluaciones
# o mas.
#
def setArticulosAceptables():
    listaArticulos = []
    #Se toman todos los articulos que tienen promedio mayor a 3.00
    try:
        #Article.objects.all().annotate(arbitros_count=Count('keywords__keyword'))
        evaluacion = Evaluacion.objects.filter(promedio__gte = 3)
        #Si hubo resultados, se hace una iteracion para ver si tiene minimo dos evaluaciones.
        if evaluacion != None:
            for ev in evaluacion:
                if ev.arbitros.all().count() >= 2:
                    articulo = ev.articulo
                    articulo.aceptable = True
                    articulo.save()
                    listaArticulos.append(articulo)
        if len(evaluacion) == 0:
            evaluacion = None
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
        for emp in empatados:
            articulo = getArticuloPorId(emp.pk)
            if articulo != None:
                articulo.empatado = True
                articulo.save()
        return empatados

def generarAceptados(aceptables):
    # Se verifica si el maximo de articulos es mayor que la longitud de la lista de aceptables
    # si esto pasa entonces la lista de aceptables pasa a ser la lista de aceptados, sino se busca
    # cual es la nueva lista de aceptados
    maxarticulos = getDatosConferencia()
    if maxarticulos>=len(aceptables):
        for art in aceptables:
            articulo = getArticuloPorId(art.pk)
            if articulo != None:
                articulo.aceptado = True
                articulo.save()
        return aceptables
    else:
        if maxarticulos > 0:
            aceptados=[]
            i=0
            while i<maxarticulos:
                aceptados.append(aceptables[i])
                aceptables[i].aceptado = True
                aceptables[i].save()
                i+=1
            # ultimo es el articulo con promedio de menor valor en la lista de aceptados
            ultimo=aceptados[maxarticulos-1]
            evalUltimo = ultimo.evaluacion
            # se cuenta cuantas veces aparece el promedio en la lista de aceptados
            numvecesaccept=calcular_ocurrencia(evalUltimo.promedio, aceptados)
            # se cuenta cuantas veces aparece el promedio en la lista de aceptables
            numvecesaceptables=calcular_ocurrencia(evalUltimo.promedio, aceptables)
            # si el numero de veces de aceptados es distinto del numero de veces de aceptables
            # se procede a eliminar todos los valores que fueron admitidos en la lista de aceptados
            
            if numvecesaccept!=numvecesaceptables:
                promedioEmpatado = evalUltimo.promedio
                aceptados.remove(ultimo)
                ultimo.aceptado = False
                ultimo.save()
                for articulo in aceptados:
                    if(articulo.evaluacion.promedio == promedioEmpatado):
                        aceptados.remove(articulo)
                        articulo.aceptado = False
                        articulo.save()
        else:
            return []
    return aceptados

def generarListas():
    listaAceptables = setArticulosAceptables()
    listaAceptables = sorted(listaAceptables,key= lambda element: getEvaluacionesDeArticulo(element.pk).promedio, reverse = True)
    articulosAceptados = generarAceptados(listaAceptables)
    articuloEmpatado = get_empatados(articulosAceptados, listaAceptables)
    return {'listaAceptables':listaAceptables, 'articulosAceptados':articulosAceptados, 'articuloEmpatado':articuloEmpatado}
    
def aceptablesNota(request):
    if getArticulosAceptados()==None:
        listas = generarListas()
        context = RequestContext(request, {
                    'articuloAceptable'    : listas['listaAceptables'],
                    'articuloAceptado'     : listas['articulosAceptados'],
                    'articuloEmpatado'     : listas['articuloEmpatado'],
        })
        return render(request, 'Conferencia/aceptables.html', context)
    else:
        articulosAceptados = getArticulosAceptados()
        articulosEmpatados = getArticulosEmpatados()
        context = RequestContext(request, {
                'articulosAceptados'    : articulosAceptados,
                'articulosEmpatados'    : articulosEmpatados,
        })
        return render(request, 'Conferencia/tiposDeSeleccionar.html', context)

def mostrarFormComprobar(request):
    form = CorreoForm()
    return render(request, 'Conferencia/comprobarPresidente.html', {'form':form})

def comprobarPresidente(request):
    form = CorreoForm()
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            correoForm = form.cleaned_data['correo']
            per = getPersona(correoForm)    
            if per != None:
                com = getComite(correoForm)
                if com == None:
                    form = CorreoForm()
                    return render(request, 'Conferencia/comprobarPresidente.html', 
                  {'form':form, 
                   'error_message' : "No hay ningun miembro del comite con ese correo"})
                else:
                    if com.presidente:
                        listaAceptados = getArticulosAceptados()
                        listaEmpatados = getArticulosEmpatados()
                        maxarticulos = getDatosConferencia()
                        if listaAceptados != None:
                            cantidad = maxarticulos - len(listaAceptados)
                        else:
                            cantidad = maxarticulos
                        return render(request, 'Conferencia/desempatar.html', {'listaAceptados':listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad})             
                    else:
                        form = CorreoForm()
                        return render(request, 'Conferencia/comprobarPresidente.html', {'form':form, 'error_message' : "El miembro del comite debe ser el presidente."})
        else:
            form = CorreoForm()
    return render(request, 'Conferencia/comprobarPresidente.html', 
                  {'form':form, 
                   'error_message' : "Coloque un email valido."})

def agregarAceptado(request, articulo_id):
    listaAceptados = getArticulosAceptados()
    listaEmpatados = getArticulosEmpatados()
    maxarticulos = getDatosConferencia()
    if listaAceptados == None:
        listaAceptados = []
        
    if maxarticulos > len(listaAceptados):
        articulo = getArticuloPorId(articulo_id)
        if articulo != None:
            articulo.aceptado = True
            articulo.empatado = False
            articulo.save()
        listaAceptados = getArticulosAceptados()
        listaEmpatados = getArticulosEmpatados()
        maxarticulos = getDatosConferencia()
        cantidad = maxarticulos - len(listaAceptados)
        return render(request, 'Conferencia/desempatar.html', {'listaAceptados':listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad})
    maxarticulos = getDatosConferencia()
    cantidad = maxarticulos - len(listaAceptados)
    return render(request, 'Conferencia/desempatar.html', 
                  {'listaAceptados':listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad, 
                   'error_message' : "Ya no se puede aceptar mas articulos."})
    
def limpiarArticulos(listA, listE):
    if listA != None:
        for acept in listA:
            articulo = getArticuloPorId(acept.pk)
            if articulo != None:
                articulo.aceptado = False
                articulo.save()
    if listE != None:
         for acept in listE:
            articulo = getArticuloPorId(acept.pk)
            if articulo != None:
                articulo.empatado = False
                articulo.save()
                    
def reiniciarSeleccion(request):
    limpiarArticulos(getArticulosAceptados(), getArticulosEmpatados())
    conferencia = Conferencia.objects.all()
    context = RequestContext(request, {
            'conferencia'    : conferencia,
    })
    return render(request, 'Conferencia/index.html', context)

def desempatar(request):
    listaAceptados = getArticulosAceptados()
    listaEmpatados = getArticulosEmpatados()
    maxarticulos = getDatosConferencia()
    cantidad = maxarticulos - len(listaAceptados)
    return render(request, 'Conferencia/desempatar.html', {'listaAceptados': listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad})