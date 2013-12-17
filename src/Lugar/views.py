from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from Lugar.models import Lugar
from Evento.forms import EventoForm
from Evento.models import Apertura, Clausura, Taller, Ponencia, CharlaInvitada, EventoSocial

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
    form = EventoForm()
    return render(request, 'Lugar/mostrarFormEvento.html', {'form':form, 'lugar_id':lugar_id, 'evento_tipo':evento_tipo,})

def definirEvento(request, lugar_id):
    return render(request, 'Lugar/definirEvento.html',{'lugar_id':lugar_id})

def asignar(request, lugar_id, evento_tipo):
    lugar = get_object_or_404(Lugar, pk=lugar_id)
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            if(evento_tipo == 'apertura'):
                evento = Apertura()
                evento.lugar = lugar
                evento.titulo = form.cleaned_data['titulo']
                evento.duracion = form.cleaned_data['duracion']
                evento.fechaIni = form.cleaned_data['fechaIni']
                evento.horaIni = form.cleaned_data['horaIni']
                evento.save()
                return HttpResponseRedirect(reverse('Lugar:detalle', args=(lugar_id)))
            elif(evento_tipo == 'clausura'):
                evento = Clausura()
                evento.lugar = lugar
                evento.titulo = form.cleaned_data['titulo']
                evento.duracion = form.cleaned_data['duracion']
                evento.fechaIni = form.cleaned_data['fechaIni']
                evento.horaIni = form.cleaned_data['horaIni']
                evento.save()
                return HttpResponseRedirect(reverse('Lugar:detalle', args=(lugar_id)))
            elif(evento_tipo == 'taller'):
                evento = Taller()
                evento.lugar = lugar
                evento.titulo = form.cleaned_data['titulo']
                evento.duracion = form.cleaned_data['duracion']
                evento.fechaIni = form.cleaned_data['fechaIni']
                evento.horaIni = form.cleaned_data['horaIni']
                evento.save()
                return HttpResponseRedirect(reverse('Lugar:detalle', args=(lugar_id)))
            elif(evento_tipo == 'ponencia'):
                evento = Ponencia()
                evento.lugar = lugar
                evento.titulo = form.cleaned_data['titulo']
                evento.duracion = form.cleaned_data['duracion']
                evento.fechaIni = form.cleaned_data['fechaIni']
                evento.horaIni = form.cleaned_data['horaIni']
                evento.save()
                return HttpResponseRedirect(reverse('Lugar:detalle', args=(lugar_id)))
            elif(evento_tipo == 'charlaInvitada'):
                evento = CharlaInvitada()
                evento.lugar = lugar
                evento.titulo = form.cleaned_data['titulo']
                evento.duracion = form.cleaned_data['duracion']
                evento.fechaIni = form.cleaned_data['fechaIni']
                evento.horaIni = form.cleaned_data['horaIni']
                evento.save()
                return HttpResponseRedirect(reverse('Lugar:detalle', args=(lugar_id)))
            elif(evento_tipo == 'eventoSocial'):
                evento = EventoSocial()
                evento.lugar = lugar
                evento.titulo = form.cleaned_data['titulo']
                evento.duracion = form.cleaned_data['duracion']
                evento.fechaIni = form.cleaned_data['fechaIni']
                evento.horaIni = form.cleaned_data['horaIni']
                evento.save()
                return HttpResponseRedirect(reverse('Lugar:detalle', args=(lugar_id)))
            else:
                return HttpResponse
        else:
            form = EventoForm()
            
    return render(request, 'Lugar/mostrarFormEvento.html', 
                  {'form':form, 
                   'error_message' : "No se lleno el formulario correctamente. La duracion tiene que ser un entero, la fecha de inicio una fecha valida, y la hora de inicio una hora valida.",
                   'lugar_id':lugar_id, 
                   'evento_tipo':evento_tipo,})
