# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from Articulo.models import Articulo
from django.core.urlresolvers import reverse
#from Topico.forms import TopicoForm

def indice(request):
    articulos= []#Articulo.objects.all()
    context=RequestContext(request, {
            'articulos' : articulos
    })
    return render(request,'Articulo/index.html',{})
