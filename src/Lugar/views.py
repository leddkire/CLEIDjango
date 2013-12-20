from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.db import IntegrityError

from Lugar.models import Lugar
from Lugar.forms import LugarForm
from Evento.forms import EventoFormParaLugar
from Evento.models import Apertura, Clausura, Taller, Ponencia, CharlaInvitada, EventoSocial
from Evento.funciones import existe, existeApertura, existeClausura

def indice(request):
    listaLugares = Lugar.objects.all()
    context = RequestContext(request, {
            'listaLugares': listaLugares,
    })
    return render(request, 'Lugar/index.html', context)

def detalle(request, lugar_id):
    lugar= get_object_or_404(Lugar, pk=lugar_id)
    return render(request, 'Lugar/detalle.html',{'lugar': lugar})

def eventosDeLugar(request, lugar_id):
    return HttpResponse("Estas viendo los eventos asignados a este lugar: %s" %lugar_id)

def mostrarFormEvento(request, lugar_id, evento_tipo):
    form = EventoFormParaLugar()
    return render(request, 'Lugar/mostrarFormEvento.html', {'form':form, 'lugar_id':lugar_id, 'evento_tipo':evento_tipo,})

def definirEvento(request, lugar_id):
    return render(request, 'Lugar/definirEvento.html',{'lugar_id':lugar_id})

def asignar(request, lugar_id, evento_tipo):
    def armarEntidad(lugar, evento):
        evento.lugar = lugar
        evento.titulo = form.cleaned_data['titulo']
        evento.duracion = form.cleaned_data['duracion']
        evento.fechaIni = form.cleaned_data['fechaIni']
        evento.horaIni = form.cleaned_data['horaIni']
        evento.save()
    lugar = get_object_or_404(Lugar, pk=lugar_id)
    if request.method == 'POST':
        form = EventoFormParaLugar(request.POST)
        if form.is_valid():
            if not(existe(form.cleaned_data['titulo'])):
                if evento_tipo == 'apertura':
                    if not existeApertura():
                        evento = Apertura()
                        armarEntidad(lugar,evento)
                        return HttpResponseRedirect(reverse('Lugar:index'))
                    else:
                        error_message = "Ya existe un evento de apertura en el CLEI"
                elif evento_tipo == 'clausura':
                    if not existeClausura():
                        evento = Clausura()
                        armarEntidad(lugar,evento)
                        return HttpResponseRedirect(reverse('Lugar:index'))
                    else:
                        error_message="Ya existe un evento de clausura en el CLEI"
                elif evento_tipo == 'taller':
                    evento = Taller()
                    armarEntidad(lugar,evento)
                    return HttpResponseRedirect(reverse('Lugar:index'))
                elif evento_tipo == 'ponencia':
                    evento = Ponencia()
                    armarEntidad(lugar,evento)
                    return HttpResponseRedirect(reverse('Lugar:index'))
                elif evento_tipo == 'charlaInvitada':
                    evento = CharlaInvitada()
                    armarEntidad(lugar,evento)
                    return HttpResponseRedirect(reverse('Lugar:index'))
                elif evento_tipo == 'eventoSocial':
                    evento = EventoSocial()
                    armarEntidad(lugar,evento)
                    return HttpResponseRedirect(reverse('Lugar:index'))
                else:
                    return HttpResponse("Error.")
            else:
                error_message="Un evento con ese titulo ya existe."
                
        else:
            error_message="No se lleno el formulario correctamente. La duracion tiene que ser un entero, la fecha de inicio una fecha valida, y la hora de inicio una hora valida."

    form = EventoFormParaLugar()
    return render(request, 'Lugar/mostrarFormEvento.html', 
                  {'form':form, 
                   'error_message' : error_message,
                   'lugar_id':lugar_id, 
                   'evento_tipo':evento_tipo,})

def crear(request):
    form = LugarForm()
    return render(request, 'Lugar/crear.html', {'form':form})

def guardar(request):
    if request.method == 'POST':
        form = LugarForm(request.POST)
        if form.is_valid():
            try:
                lugar = Lugar()
                lugar.nombre = form.cleaned_data['nombre']
                lugar.ubicacion = form.cleaned_data['ubicacion']
                lugar.capacidadMax = form.cleaned_data['capacidadMax']
                lugar.save()
                return HttpResponseRedirect(reverse('Lugar:index'))
            except IntegrityError: 
                return render(request, 'Lugar/crear.html', {'error_message':'El lugar ya existe.'})
        else:
            return render(request, 'Lugar/crear.html', {'error_message':'Datos ingresados no son validos.',
                                                        'form':form})
    
