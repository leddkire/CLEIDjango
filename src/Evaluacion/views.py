# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from Evaluacion.models import Evaluacion,Nota
from django.core.urlresolvers import reverse
from Evaluacion.forms import EvaluacionForm
from Articulo.models import Articulo
from funciones import existe
from Comite.models import Comite

def indice(request):
    evaluaciones= Evaluacion.objects.all()
    context=RequestContext(request, {
            'evaluaciones' : evaluaciones
    })
    return render(request,'Evaluacion/index.html',context)

def detalle(request, clave):
    evaluacion = Evaluacion.objects.get(pk=clave)
    notas= evaluacion.notas.all()
    
    arbitros = evaluacion.arbitros.all()
    promedio= evaluacion.promedio
    titulo = evaluacion.articulo.titulo
    context=RequestContext(request, {
            'notas' : notas,
            'arbitros' : arbitros,
            'promedio' : promedio,
            'titulo' : titulo,
    })
    return render(request, 'Evaluacion/detalle.html', context)

def mostrarFormEvaluacion(request):
    form = EvaluacionForm(initial={'articulo':"Probando"})
    return render(request, 'Evaluacion/crearEvaluacion.html', {'form':form} )

def mostrarArbitro(request):
    #arbitros = Arbitro.objects.all()
    arbitros = Comite.objects.filter(arbitro=True) 
    context=RequestContext(request, {
            'arbitros' : arbitros,
    })
    return render(request, 'Evaluacion/mostrarArbitro.html', context )

def mostrarArticulo(request,arbitro_id):
    articulos = Articulo.objects.all()
    context=RequestContext(request, {
            'articulos' : articulos,
            'arbitro_id': arbitro_id,
    })
    return render(request, 'Evaluacion/mostrarArticulo.html', context )

def mostrarFormEvaluar(request,articulo_id,arbitro_id):#,articulo_id):
    articulo = get_object_or_404(Articulo,pk=articulo_id)
    arbitro = get_object_or_404(Comite,pk=arbitro_id)
    form = EvaluacionForm()
    context=RequestContext(request, {
            'articulo' : articulo,
            'arbitro': arbitro,
            'form': form,
    })
    return render(request, 'Evaluacion/mostrarFormEvaluacion.html', context )

def crearEvaluacion(request,arbitro,articulo):
    def calcularPromedio(arrayNotas):
        prom=0
        for x in arrayNotas:
            prom+=x.valor
        prom=float(prom)/len(arrayNotas)
        prom=round(prom,2)
        return prom
    
    def armarEntidad(evaluacion):
        #Obtenemos el objeto articulo con el nombre
        
        #artObj=Articulo(titulo=articulo)
        #arbitroObj=get_object_or_404(Comite,correo=arbitro)
        arbitroObj=Comite.objects.get(correo=arbitro)
        evaluacion.arbitros.add(arbitroObj)
        numero=form.cleaned_data['valor']
        #valorNota,creado=Nota.objects.get_or_create(valor=numero)
        valorNota=Nota(valor=numero)
        valorNota.save()
        evaluacion.notas.add(valorNota)
        arrayNotas=evaluacion.notas.all()
        prom=calcularPromedio(arrayNotas)
        evaluacion.promedio = prom
        evaluacion.save()
    if request.method =='POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            if not(existe(arbitro,articulo)):
                artObj=get_object_or_404(Articulo,titulo=articulo) 
                try:
                    evaluacion=Evaluacion.objects.get(articulo=artObj)
                except Evaluacion.DoesNotExist:
                    evaluacion = Evaluacion(articulo=artObj)
                    evaluacion.save()
                #evaluacion.articulo=artObj
                #
                armarEntidad(evaluacion)
                return HttpResponseRedirect(reverse('Evaluacion:indice'))
            else:
                error_message="Ya el arbitro evaluo este articulo"
        else:
            error_message="No se selecciono la nota"
    #verificar aqui si existe 
    form=EvaluacionForm()
    context=RequestContext(request, {
            'arbitro': arbitro,
            'articulo' : articulo,
            'form': form,
            'error_message' :error_message,
    })
    return render(request,'Evaluacion/mostrarFormEvaluacion.html',context)