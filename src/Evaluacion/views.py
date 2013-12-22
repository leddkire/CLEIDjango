# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from Evaluacion.models import Evaluacion
from django.core.urlresolvers import reverse
from Evaluacion.forms import EvaluacionForm


def indice(request):
    evaluaciones= Evaluacion.objects.all()
    context=RequestContext(request, {
            'evaluaciones' : evaluaciones
    })
    return render(request,'Evaluacion/index.html',context)

def mostrarFormEvaluacion(request):
    form = EvaluacionForm()
    return render(request, 'Evaluacion/crearEvaluacion.html', {'form':form} )
