# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from Evento.models import Apertura,Clausura,Taller,Ponencia,CharlaInvitada, EventoSocial
from Evento.forms import EventoForm, TallerCharlaPonenciaForm
from Evento.funciones import existe, existeApertura, existeClausura, intersectaFecha

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
    if evento_tipo =='apertura':
        if existeApertura():
            error_message = 'Ya existe un evento de apertura en el CLEI'
            return render(request, 'Evento/definirEvento.html',{'error_message':error_message})
    if evento_tipo =='clausura':
        if existeClausura():
            error_message = 'Ya existe un evento de clausura en el CLEI'
            return render(request, 'Evento/definirEvento.html',{'error_message':error_message})
    #Revisar cual tipo de evento es para crear el formulario apropiado
    if (evento_tipo == 'charlaInvitada' or 
        evento_tipo == 'taller' or evento_tipo == 'ponencia'):
        form = TallerCharlaPonenciaForm
    else:
        form = EventoForm()
    return render(request, 'Evento/mostrarFormEvento.html', {'form':form,'evento_tipo':evento_tipo,})

def crear(request, evento_tipo):
    def armarEntidad(evento):
        evento.lugar = form.cleaned_data['lugar']
        evento.titulo = form.cleaned_data['titulo']
        evento.duracion = form.cleaned_data['duracion']
        evento.fechaIni = form.cleaned_data['fechaIni']
        evento.horaIni = form.cleaned_data['horaIni']
        if (evento_tipo == 'charlaInvitada' or 
        evento_tipo == 'taller' or evento_tipo == 'ponencia'):
            evento.topico = form.cleaned_data['topico']
        evento.save()  
    if request.method == 'POST':
        if (evento_tipo == 'charlaInvitada' or 
        evento_tipo == 'taller' or evento_tipo == 'ponencia'):
            form = TallerCharlaPonenciaForm(request.POST)
        else:
            form = EventoForm(request.POST)
        if form.is_valid():
            if not(existe(form.cleaned_data['titulo'])):
                if not(intersectaFecha(form.cleaned_data['fechaIni'],form.cleaned_data['horaIni'],form.cleaned_data['lugar'], form.cleaned_data['duracion'])):
                    if evento_tipo == 'apertura':
                        if not existeApertura():
                            evento = Apertura()
                            armarEntidad(evento)
                            return HttpResponseRedirect(reverse('Evento:indice'))
                        else:
                            err = "Ya existe un evento de apertura en el CLEI"
                    elif evento_tipo == 'clausura':
                        if not existeClausura():
                            evento = Clausura()
                            armarEntidad(evento)
                            return HttpResponseRedirect(reverse('Evento:indice'))
                        else:
                            err="Ya existe un evento de clausura en el CLEI"
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
                    err = "En el lugar asignado existe un evento que termina o comienza dentro de la hora y fecha establecida"
            else:
                err ="Un evento con este titulo ya existe."
                
        else:
            err = "No se lleno el formulario correctamente." 
    error_message = err       
    return render(request, 'Evento/mostrarFormEvento.html', 
                  {'form':form, 
                   'error_message' : error_message,
                   'evento_tipo':evento_tipo,})
    
def asignarModIndex(request, evento_id, evento_tipo):
    if evento_tipo == 'ponencia':
        form = PonenciaModForm()
    elif evento_tipo == 'charlaInvitada':
        form = CharlaModForm()
    return render(request, 'Evento/asignarModIndex.html',
                  {'form': form,
                   'evento_id':evento_id,
                   'evento_tipo':evento_tipo})
    
def asignarMod(request, evento_id, evento_tipo):
    if request.method == 'POST':
        if evento_tipo == 'ponencia':
            form = PonenciaModForm(request.POST)
            evento = get_object_or_404(Ponencia,pk=evento_id)
        elif evento_tipo == 'charlaInvitada':
            form = CharlaModForm(request.POST)
            evento = get_object_or_404(CharlaInvitada,pk=evento_id)
        if form.is_valid():
            evento.moderador = form.cleaned_data['moderador']
            evento.save()
            return HttpResponseRedirect(reverse('Evento:detalle',args=[evento_id,evento_tipo]))
            
#Asignacion de articulos a los eventos
def mostrarArticulos(request,evento_tipo,evento_id):
    
def asignarArticulo(request, evento_tipo, evento_id, articulo_id):       
    