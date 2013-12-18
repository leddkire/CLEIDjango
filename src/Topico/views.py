# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from Topico.models import Topico
from django.core.urlresolvers import reverse
from Topico.forms import TopicoForm

def indice(request):
    topicos= Topico.objects.all()
    context=RequestContext(request, {
            'topicos' : topicos
    })
    return render(request,'Topico/index.html',context)

#def crearTopico(request):
#    return render(request, 'Topico/crearTopico.html', {})  

def mostrarFormTopico(request):
    form = TopicoForm()
    return render(request, 'Topico/crearTopico.html', {'form':form})

def crearTopico(request):
    def armarEntidad(topico):
        topico.nombre = form.cleaned_data['nombre']
        topico.save()
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            topico = Topico()
            armarEntidad(topico)
            return HttpResponseRedirect(reverse('Topico:indice'))
        else:
            form = EventoForm()
            
    return render(request, 'Topico/indice.html', 
                  {'form':form, 
                   'error_message' : "No se lleno el formulario correctamente.",
                   })