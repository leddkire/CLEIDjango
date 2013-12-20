# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from Articulo.models import Articulo
from Articulo.forms import ArticuloForm
#from Topico.forms import TopicoForm

def indice(request):
    articulos= Articulo.objects.all()
    context=RequestContext(request, {
            'articulos' : articulos
    })
    return render(request,'Articulo/index.html',context)

def detalle(request, articulo_id):
    articulo = get_object_or_404(Articulo,pk=articulo_id)
    return render(request, 'Articulo/detalle.html', {'articulo':articulo})

def mostrarFormArticulo(request):
    form = ArticuloForm()
    return render(request,'Articulo/mostrarFormArticulo.html',{'form':form})

def crear(request):
    if request.method=='POST':
        form =ArticuloForm(request.POST)
        if form.is_valid():
            articulo = Articulo()
            articulo.titulo = form.cleaned_data['titulo']
            articulo.palabrasClaves= form.cleaned_data['palabrasClaves']
            articulo.resumen = form.cleaned_data['resumen']
            articulo.texto = form.cleaned_data['texto']
            articulo.save()
            return HttpResponseRedirect(reverse('Articulo:indice'))
        else:
            form = ArticuloForm()
            return render(request, 'Articulo/mostrarFormArticulo.html', {'form':form,
                                                                    'error_message':'No se introdujeron los valores de manera correcta.'})
    else:
        return HttpResponse("No se recibio un formulario.")