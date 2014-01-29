from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.db import IntegrityError

from Persona.models import Persona
from Persona.forms import CorreoForm
from Comite.models import Moderador, Comite
from Evento.models import Ponencia, CharlaInvitada
def indice(request):
    ponencias = Ponencia.objects.all()
    charlas = CharlaInvitada.objects.all()
    return render(request, 'asignarModerador/indice.html',{'ponencias':ponencias,
                                                           'charlas': charlas,
                                                           })

def mostrarMods(request,evento_tipo, evento_id):
    if evento_tipo == 'ponencia':
        evento = get_object_or_404(Ponencia,pk = evento_id)
    else:
        evento = get_object_or_404(CharlaInvitada,pk = evento_id)
    if evento_tipo == 'ponencia':
        modsDeComite = Moderador.objects.filter(comite__topicos = evento.topico).exclude(ponencia = evento_id)
    else:
        modsDeComite = Moderador.objects.filter(comite__topicos = evento.topico).exclude(charlainvitada = evento_id)
    modsDeEvento = evento.moderadores.all()
    form = CorreoForm()
    return render(request, 'asignarModerador/mostrarMods.html',{'evento_tipo': evento_tipo,
                                                                'evento_id': evento_id,
                                                                'moderadores': modsDeComite,
                                                                'modsEvento':modsDeEvento,
                                                                'form' : form})
    
def asignarMod(request,evento_tipo,evento_id):
    if evento_tipo == 'ponencia':
        evento = get_object_or_404(Ponencia,pk = evento_id)
    else:
        evento = get_object_or_404(CharlaInvitada,pk = evento_id)
    error_message = ''
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            try:
                moderador = Moderador.objects.get(comite__correo__correo = form.cleaned_data['correo'])
            except(Moderador.DoesNotExist):
                moderador = None
            if(moderador == None):
                error_message = "El correo que introdujo no pertenece a ningun moderador"
            else:
                evento.moderadores.add(moderador)
                evento.save()
            #Se vuelven a cargar los datos para regresar al listado de moderadores
        else:
            error_message = "No se introdujo un correo valido."
        if evento_tipo == 'ponencia':
            modsDeComite = Moderador.objects.filter(comite__topicos = evento.topico).exclude(ponencia = evento_id)
        else:
            modsDeComite = Moderador.objects.filter(comite__topicos = evento.topico).exclude(charlainvitada = evento_id)
        modsDeEvento = evento.moderadores.all()
        return render(request, 'asignarModerador/mostrarMods.html', {'evento_tipo': evento_tipo,
                                                                'evento_id': evento_id,
                                                                'moderadores': modsDeComite,
                                                                'modsEvento':modsDeEvento,
                                                                'error_message':error_message,
                                                                'form':form,})
    
    
