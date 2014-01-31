from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import django.db.models
from operator import itemgetter

# Create your views here.
from Articulo.models import Articulo
from Topico.models import Topico
from Conferencia.models import Conferencia
from Conferencia.forms import ConferenciaForm
from Comite.forms import CorreoForm
from funciones import getArticulosAceptados
from funciones import getNumArticulosDeTopico
from funciones import getTopicos
from funciones import getArticulosNoEspeciales
from funciones import getArticulosAceptadosYEspeciales
from funciones import getArticulosAceptadosEspecial
from funciones import getArticulosRechazadosCupo
from funciones import getArticulosRechazadosPorPromedio
from Evaluacion.models import Evaluacion
from funciones import getEvaluacionesDeArticulo
from funciones import getArticuloPorId
from funciones import getArticulosAceptables
from funciones import getDatosConferencia
from funciones import getArticulosEmpatados
from funciones import getPersona
from funciones import getComite
from Evento.models import Ponencia,Taller,CharlaInvitada
from funciones import getAutor
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
        formConferencia = ConferenciaForm(initial={'anio': confe[0].anio, 'pais':confe[0].pais, 
                                                   'maxArticulos':confe[0].maxArticulos})
    else:
        formConferencia = ConferenciaForm()
    return render(request, 'Conferencia/editarDatosConferencia.html', {'formConferencia':formConferencia, })

def armarEntidad(formConferencia):
    conferencia = Conferencia()
    conferencia.anio = formConferencia.cleaned_data['anio']
    conferencia.pais = formConferencia.cleaned_data['pais']
    conferencia.maxArticulos = formConferencia.cleaned_data['maxArticulos']
        
    try:
        confe = Conferencia.objects.get(anio = conferencia.anio)
    except Conferencia.DoesNotExist:
        confe = None

    if confe != None:
        confe.anio = conferencia.anio
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
    articulosAceptados = getArticulosAceptadosYEspeciales()
    maxarticulos = getDatosConferencia()
    if articulosAceptados != None:
        cantidad = maxarticulos - len(articulosAceptados)
    else:
        cantidad = maxarticulos
    articulosEmpatados = getArticulosEmpatados()
    context = RequestContext(request, {
            'articulosAceptados'    : articulosAceptados,
            'articulosEmpatados'    : articulosEmpatados,
            'cantidad'              : cantidad
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
        rechazadosPromedio = Evaluacion.objects.filter(promedio__lte = 3)
        #Se establecen los articulos rechazados por promedio. Considerando solo los que tienen dos evaluaciones o mas.
        
        if rechazadosPromedio != None:
            for re in rechazadosPromedio:
                if re.arbitros.all().count() >= 2:
                    articulo = re.articulo
                    if articulo.aceptadoEspecial == False:
                        articulo.rechazadoPorPromedio = True
                        articulo.save()
        #Si hubo resultados, se hace una iteracion para ver si tiene minimo dos evaluaciones.
        if evaluacion != None:
            for ev in evaluacion:
                if ev.arbitros.all().count() >= 2:
                    articulo = ev.articulo
                    #Se comprueba que no se haya seleccionado antes como articulo especial.
                    if articulo.aceptadoEspecial == False:
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
                articulo.rechazadoFaltaCupo = True
                articulo.save()
        return empatados

def generarAceptados(aceptables):
    # Se verifica si el maximo de articulos es mayor que la longitud de la lista de aceptables
    # si esto pasa entonces la lista de aceptables pasa a ser la lista de aceptados, sino se busca
    # cual es la nueva lista de aceptados
    maxarticulos = getDatosConferencia()
    especiales = getArticulosAceptadosEspecial()
    if especiales != None:
        maxarticulos = maxarticulos - len(especiales)
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
            #Se establecen los rechazados por cupo
            porCupo = Evaluacion.objects.filter(promedio__gte = 3, promedio__lte = evalUltimo.promedio)
            if porCupo != None:
                for ev in porCupo:
                    if ev.arbitros.all().count() >= 2:
                        articulo = ev.articulo
                        articulo.rechazadoFaltaCupo = True
                        articulo.save()
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
        articulosAceptados = getArticulosAceptadosYEspeciales()
        articulosEmpatados = getArticulosEmpatados()
        context = RequestContext(request, {
                'articulosAceptados'    : articulosAceptados,
                'articulosEmpatados'    : articulosEmpatados,
        })
        return render(request, 'Conferencia/tiposDeSeleccionar.html', context)

def mostrarFormComprobar(request, vista_sigue):
    form = CorreoForm()
    return render(request, 'Conferencia/comprobarPresidente.html', {'form':form, 'vistaSiguiente':vista_sigue})

def comprobarPresidente(request, vista_sigue):
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
                  {'form':form, 'vistaSiguiente':vista_sigue,
                   'error_message' : "No hay ningun miembro del comite con ese correo"})
                else:
                    if com.presidente:
                        listaAceptados = getArticulosAceptadosYEspeciales()
                        listaEmpatados = getArticulosEmpatados()
                        maxarticulos = getDatosConferencia()
                        if listaAceptados != None:
                            cantidad = maxarticulos - len(listaAceptados)
                        else:
                            cantidad = maxarticulos
                        if vista_sigue == "desempatar":
                            return render(request, 'Conferencia/desempatar.html', {'listaAceptados':listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad})
                        else:
                            return render(request, 'Conferencia/especiales.html', {'listaArticulos':getArticulosNoEspeciales(), 'listaEspeciales':getArticulosAceptadosEspecial(), 'cantidad':cantidad})              
                    else:
                        form = CorreoForm()
                        return render(request, 'Conferencia/comprobarPresidente.html', {'form':form, "vistaSiguiente":vista_sigue, 'error_message' : "El miembro del comite debe ser el presidente."})
        else:
            form = CorreoForm()
    return render(request, 'Conferencia/comprobarPresidente.html', 
                  {'form':form, 'vistaSiguiente':vista_sigue,
                   'error_message' : "Coloque un email valido."})

def agregarAceptado(request, articulo_id):
    listaAceptados = getArticulosAceptadosYEspeciales()
    listaEmpatados = getArticulosEmpatados()
    maxarticulos = getDatosConferencia()
    if listaAceptados == None:
        listaAceptados = []
        
    if maxarticulos > len(listaAceptados):
        articulo = getArticuloPorId(articulo_id)
        if articulo != None:
            articulo.empatado = False
            articulo.rechazadoFaltaCupo = False
            articulo.aceptado = True
            articulo.save()
        listaAceptados = getArticulosAceptadosYEspeciales()
        listaEmpatados = getArticulosEmpatados()
        maxarticulos = getDatosConferencia()
        cantidad = maxarticulos - len(listaAceptados)
        return render(request, 'Conferencia/desempatar.html', {'listaAceptados':listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad})
    maxarticulos = getDatosConferencia()
    cantidad = maxarticulos - len(listaAceptados)
    return render(request, 'Conferencia/desempatar.html', 
                  {'listaAceptados':listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad, 
                   'error_message' : "Ya no se puede aceptar mas articulos."})
    
def limpiarArticulos(listA, listE, listAE, listRC, listRP):
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
    if listAE != None:
         for acept in listAE:
            articulo = getArticuloPorId(acept.pk)
            if articulo != None:
                articulo.aceptadoEspecial = False
                articulo.save()
    if listRC != None:  
         for acept in listRC:
            articulo = getArticuloPorId(acept.pk)
            if articulo != None:
                articulo.rechazadoFaltaCupo = False
                articulo.save()
    if listRP != None:  
         for acept in listRP:
            articulo = getArticuloPorId(acept.pk)
            if articulo != None:
                articulo.rechazadoPorPromedio = False
                articulo.save()                       
def reiniciarSeleccion(request):
    limpiarArticulos(getArticulosAceptados(), getArticulosEmpatados(), getArticulosAceptadosEspecial(), getArticulosRechazadosCupo(), getArticulosRechazadosPorPromedio())
    conferencia = Conferencia.objects.all()
    context = RequestContext(request, {
            'conferencia'    : conferencia,
    })
    return render(request, 'Conferencia/index.html', context)

def generarListaArticulos(request):
    return True
    
def desempatar(request):
    listaAceptados = getArticulosAceptadosYEspeciales()
    listaEmpatados = getArticulosEmpatados()
    maxarticulos = getDatosConferencia()
    if listaAceptados != None:
        cantidad = maxarticulos - len(listaAceptados)
    else:
        cantidad = maxarticulos
    return render(request, 'Conferencia/desempatar.html', {'listaAceptados': listaAceptados, 'listaEmpatados':listaEmpatados, 'articulosRestantes':cantidad})

def mostrarEstadoArticulos(request):
    listAceptados = getArticulosAceptados()
    listAceptadosEspeciales = getArticulosAceptadosEspecial()
    listRechazadoCupo = getArticulosRechazadosCupo()
    return render(request, 'Conferencia/estadoArticulos.html', {'listAceptados': listAceptados, 'listAceptadosEspeciales': listAceptadosEspeciales, 
                                                                'listRechazadosCupo': listRechazadoCupo, 'listRechazadosPromedio':getArticulosRechazadosPorPromedio()})

def elegirEspeciales(request):
    listaAceptados = getArticulosAceptadosYEspeciales()
    maxarticulos = getDatosConferencia()
    if listaAceptados != None:
        cantidad = maxarticulos - len(listaAceptados)
    else:
        cantidad = maxarticulos
    return render(request, 'Conferencia/especiales.html', {'listaArticulos': getArticulosNoEspeciales(), 'listaEspeciales': articulosEspeciales, 'cantidad': cantidad})

def agregarEspecial(request, articulo_id):
    listaAceptados = getArticulosAceptadosYEspeciales()
    listaEmpatados = getArticulosEmpatados()
    maxarticulos = getDatosConferencia()
    if listaAceptados == None:
        listaAceptados = []
        
    if maxarticulos > len(listaAceptados):
        articulo = getArticuloPorId(articulo_id)
        if articulo != None:
            articulo.aceptadoEspecial = True
            articulo.rechazadoPorPromedio = False
            articulo.rechazadoFaltaCupo = False
            articulo.empatado = False
            articulo.save()
        listaAceptados = getArticulosAceptadosYEspeciales()
        maxarticulos = getDatosConferencia()
        cantidad = maxarticulos - len(listaAceptados)
        return render(request, 'Conferencia/especiales.html', {'listaArticulos':getArticulosNoEspeciales(), 'listaEspeciales':getArticulosAceptadosEspecial(), 'cantidad':cantidad})
    maxarticulos = getDatosConferencia()
    if listaAceptados != None:
        cantidad = maxarticulos - len(listaAceptados)
    else:
        cantidad = maxarticulos
    return render(request, 'Conferencia/especiales.html', 
                  {'listaArticulos':getArticulosNoEspeciales(), 'listaEspeciales':articulosEspeciales, 'cantidad':cantidad, 
                   'error_message' : "Ya no se pueden aceptar mas articulos."})
#EEEEEEEEEEERRRRRRRROOOOOOOOOOORRRRRRRRRRRRR
def llenarDiccionarioTopicos(request):
    listaTopicos = []
    topicos = getTopicos()
    #Se hace una lista con todos los topicos que puede haber en la conferencia y se le asigna la cantidad de
    #articulos aceptados con ese topico
    if topicos != None:
        for top in topicos:
            listaTopicos = listaTopicos+[[top.nombre, getNumArticulosDeTopico(top.nombre)]]
    #Se ordena de topico que tiene menor cantidad de articulos a mayor cantidad
    listaTopicos.sort(key=itemgetter(1))
    #Se calculan cuantos articulos faltan por aceptar
    listaAceptados = getArticulosAceptadosYEspeciales()
    maxarticulos = getDatosConferencia()
    if listaAceptados != None:
        maxarticulos = maxarticulos - len(listaAceptados)
    i = 0
    topicoValido = False
    #Se itera entre todos los topicos, tomando el que tiene menor cantidad de articulos aceptados primero
    while i < len(listaTopicos):
        if maxarticulos != 0:
            elem = listaTopicos[i]
            empatados = getArticulosEmpatados()
            if empatados != None:
                j = 0
                #Se itera sobre los articulos empatados y si hay uno que contenga el topico elegido en
                #la iteracion externa, se acepta y se rompe el ciclo.
                while j < len(empatados):
                    
                    try:
                        articulo = empatados[j]
                        topicoValido = False
                        top = articulo.topicos.get(nombre = elem[0])
                        articulo.empatado = False
                        articulo.rechazadoFaltaCupo = False
                        articulo.aceptado = True
                        articulo.save()
                        maxarticulos = maxarticulos - 1
                        elem[1] += 1
                        topicoValido = True
                        j = len(empatados)
                    except Topico.DoesNotExist:
                        pass
                    j += 1
            else:
                break
            #topicoValido indica si se encontro un articulo entre empatados con el topico seleccionado, en caso
            #de haber encontrado uno, se ordena de nuevo la lista de manera que quede el topico con menos articulos
            #de primero y se sigue en la misma posicion. En caso no haber encontrado ninguno, se pasa al siguiente topico.
            if not topicoValido:
                i += 1
            else:
                listaTopicos.sort(key=itemgetter(1))
        else:
            i = len(listaTopicos)
            break
    return render(request, 'Conferencia/desempatarPorTopico.html', {'listaAceptados': getArticulosAceptadosYEspeciales(), 'articulosRestantes':maxarticulos})
    
def pedirTipoDeEvento(request):
        return render(request,'Conferencia/pedirTipoDeEvento.html')

def generarListaArticulosSesion(request,evento_tipo):    
    if(evento_tipo == 'ponencia'):
        eventos = Ponencia.objects.all()
    elif evento_tipo == 'taller':
        eventos = Taller.objects.all()
    elif evento_tipo == 'charlaInvitada':
        eventos = CharlaInvitada.objects.all()
    return render(request,'Conferencia/mostrarListaArticulosSesion.html',{'eventos':eventos})

def desempatarPorPaises(request):
    # lista de lista que tendra asociado al articulo con el pais
    listaFinal = []
    listaArticulos = []
    # lista de lista que tendra los paises con la cantidad(numero) de articulos
    listaPaises = []
    autores = []
    listaArticulos = getArticulosAceptables()
    if listaArticulos != None:
        for articulo in listaArticulos:
            # lista temporal que almacena a cada articulo los paises de sus autores
            listaTemp = []
            autores = articulo.autores.all()
            listaTemp += [articulo]
            for person in autores:
                try:
                    country = person.persona.pais
                except Persona.DoesNotExist:
                    pass
                listaTemp += [country]
                flag = False
                for lista in listaPaises:
                    # en la posicion 0 de la lista estaran los paises, en la 1 el numero de veces
                    if lista[0] == country:
                        if articulo.aceptado == True:
                            lista[1] += 1
                        flag = True
                    else:
                        flag = False
                # forma de llenar la lista de paises
                if flag == False:
                    if articulo.aceptado == True:
                        listaPaises += [[country,1]]
                    else:
                        listaPaises += [[country,0]]
            listaFinal += [listaTemp]
    #Se ordena por paises que tienen menor cantidad de articulos a mayor cantidad
    listaPaises.sort(key=itemgetter(1))
    #Se calculan cuantos articulos faltan por aceptar
    listaAceptados = getArticulosAceptados()
    maxarticulos = getDatosConferencia()
    if listaAceptados != None:
        maxarticulos = maxarticulos - len(listaAceptados)
    i = 0
    paisValido = False
    #Se itera entre todos los paises, tomando el que tiene menor cantidad de articulos aceptados primero
    while i < len(listaPaises):
        if maxarticulos != 0:
            elem = listaPaises[i]
            empatados = getArticulosEmpatados()
            if empatados != None:
                j = 0
                #Se itera sobre los articulos empatados y si hay uno que contenga el pais elegido en
                #la iteracion externa, se acepta y se rompe el ciclo.
                while j < len(listaFinal):  
                    list = listaFinal[j]
                    print list
                    if elem[0] in list:
                        paisValido = False
                        if list[0].empatado==True:                               
                            list[0].empatado = False
                            list[0].rechazadoFaltaCupo = False
                            list[0].aceptado = True
                            list[0].save()
                            maxarticulos = maxarticulos - 1
                            elem[1] += 1
                            paisValido = True
                            j = len(listaFinal)
                    j += 1
            else:
                break
            #paisValido indica si se encontro un articulo entre empatados con el pais seleccionado, en caso
            #de haber encontrado uno, se ordena de nuevo la lista de manera que quede el pais con menos articulos
            #de primero y se sigue en la misma posicion. En caso no haber encontrado ninguno, se pasa al siguiente pais.
            if not paisValido:
                i += 1
            else:
                listaPaises.sort(key=itemgetter(1))
        else:
            i = len(listaPaises)
            break
    return render(request, 'Conferencia/desempatarPorPais.html', {'listaAceptados': getArticulosAceptados(), 'articulosRestantes':maxarticulos})
