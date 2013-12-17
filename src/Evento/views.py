# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from Evento.models import Apertura,Clausura,Taller,Ponencia,CharlaInvitada, EventoSocial

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
    return HttpResponse("Indisventos.")