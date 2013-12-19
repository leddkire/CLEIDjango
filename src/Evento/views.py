# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from Evento.models import Apertura,Clausura,Taller,Ponencia,CharlaInvitada, EventoSocial
from Evento.forms import EventoForm
from Evento.funciones import existe

def indice(request):
    apertura = Apertura.objects.all()
    clausura = Clausura.objects.all()
    talleres = Taller.objects.all()
    ponencias = Ponencia.objects.all()
    charlasInvitadas = CharlaInvitada.objects.all()
    eventosSociales = EventoSocial.objects.all()
    context = RequestContext(request, {
            'apertura'        : apertura,
            'clausura'        : clausura,
            'talleres'        : talleres,
            'ponencias'       : ponencias,
            'charlasInvitadas': charlasInvitadas,
            'eventosSociales' : eventosSociales,
    })
    return render(request, 'Evento/index.html', context)


def detalle(request, evento_id, evento_tipo):
    if(evento_tipo == 'apertura'):
        evento = get_object_or_404(Apertura,pk=evento_id)
        return render(request, 'Evento/detalle.html', {'evento':evento, 'evento_id': evento_id})
    elif(evento_tipo == 'clausura'):
        evento = get_object_or_404(Clausura,pk=evento_id)
        return render(request, 'Evento/detalle.html', {'evento':evento, 'evento_id': evento_id})
    elif(evento_tipo == 'taller'):
        evento = get_object_or_404(Taller,pk=evento_id)
        return render(request, 'Evento/detalle.html', {'evento':evento, 'evento_id': evento_id})
    elif(evento_tipo == 'ponencia'):
        evento = get_object_or_404(Ponencia,pk=evento_id)
        return render(request, 'Evento/detalle.html', {'evento':evento, 'evento_id': evento_id})
    elif(evento_tipo == 'charlaInvitada'):
        evento = get_object_or_404(CharlaInvitada,pk=evento_id)
        return render(request, 'Evento/detalle.html', {'evento':evento, 'evento_id': evento_id})
    elif(evento_tipo == 'eventoSocial'):
        evento = get_object_or_404(EventoSocial,pk=evento_id)
        return render(request, 'Evento/detalle.html', {'evento':evento, 'evento_id': evento_id})
    else:
        return HttpResponse("Error al definir un evento.")

def definirEvento(request):
    return render(request, 'Evento/definirEvento.html', {})

def mostrarFormEvento(request, evento_tipo):
    form = EventoForm()
    return render(request, 'Evento/mostrarFormEvento.html', {'form':form,'evento_tipo':evento_tipo,})

def crear(request, evento_tipo):
    def armarEntidad(evento):
        evento.lugar = form.cleaned_data['lugar']
        evento.titulo = form.cleaned_data['titulo']
        evento.duracion = form.cleaned_data['duracion']
        evento.fechaIni = form.cleaned_data['fechaIni']
        evento.horaIni = form.cleaned_data['horaIni']
        evento.save()  
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            if not existe(form.cleaned_data['titulo']):
                if evento_tipo == 'apertura':
                    evento = Apertura()
                    armarEntidad(evento)
                    return HttpResponseRedirect(reverse('Evento:indice'))
                elif evento_tipo == 'clausura':
                    evento = Clausura()
                    armarEntidad(evento)
                    return HttpResponseRedirect(reverse('Evento:indice'))
                elif evento_tipo == 'taller':
                    evento = Taller()
                    armarEntidad(evento)
                    return HttpResponseRedirect(reverse('Evento:indice'))
                elif evento_tipo == 'ponencia':
                    evento = Ponencia()
                    armarEntidad(evento)
                    return HttpResponseRedirect(reverse('Evento:indice'))
                elif evento_tipo == 'charlaInvitada':
                    evento = CharlaInvitada()
                    armarEntidad(evento)
                    return HttpResponseRedirect(reverse('Evento:indice'))
                elif evento_tipo == 'eventoSocial':
                    evento = EventoSocial()
                    armarEntidad(evento)
                    return HttpResponseRedirect(reverse('Evento:indice'))
            else:
                error_message ="Un evento con este titulo ya existe."
        else:
            error_mesage = "No se lleno el formulario correctamente. La duracion tiene que ser un entero, la fecha de inicio una fecha valida, y la hora de inicio una hora valida." 
                   
    form = EventoForm()        
    return render(request, 'Evento/mostrarFormEvento.html', 
                  {'form':form, 
                   'error_message' : error_message,
                   'evento_tipo':evento_tipo,})