# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse


from Articulo.forms import ArticuloForm
from Persona.forms import PersonaForm, CorreoForm
from Topico.forms import TopicoForm
from Persona.models import Persona
from Autor.models import Autor
from Articulo.models import Articulo
from Topico.models import Topico

def indice(request):
    articulos= Articulo.objects.all()
    context=RequestContext(request, {
            'articulos' : articulos
    })
    return render(request,'Articulo/index.html',context)

def detalle(request, articulo_id):
    articulo = get_object_or_404(Articulo,pk=articulo_id)
    palabrasClavesLista = articulo.palabrasClaves.split(',')
    return render(request, 'Articulo/detalle.html', {'articulo':articulo,
                                                     'palabrasClavesLista':palabrasClavesLista,})

def crearArticuloPasoAutor(request):
    articulo = Articulo()
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            if Articulo.objects.filter(titulo = form.cleaned_data['titulo']).exists():
               error_message='Un articulo con este titulo ya existe'
               return render(request,'Articulo/crearArticuloPasoDG.html',{'form':form,
                                                                          'error_message':error_message})
            
            if(len(form.cleaned_data['palabrasClaves'].split(',')) > 5):
                error_message = 'El articulo no puede tener mas de 5 palabras claves'
                return render(request,'Articulo/crearArticuloPasoDG.html',{'form':form,
                                                                          'error_message':error_message})
            articulo.titulo = form.cleaned_data['titulo']
            articulo.palabrasClaves = form.cleaned_data['palabrasClaves']
            articulo.resumen = form.cleaned_data['resumen']
            articulo.texto = form.cleaned_data['texto']
            articulo.save()
            correoForm = CorreoForm()
            return render(request, 'Articulo/crearArticuloPasoAutor.html',{'articulo_id':articulo.id,
                                                                       'correoForm':correoForm})
        else:
            correoForm = CorreoForm()
            return render(request, 'Articulo/crearArticuloPasoDG.html',{'form':form,
                                                                        'correoForm':correoForm})
            
def crearArticuloPasoTopico(request,articulo_id):
    form = TopicoForm()
    return render(request, 'Articulo/crearArticuloPasoTopico.html', {'form':form,
                                                                     'articulo_id':articulo_id})

def crearArticuloPasoDG(request):
    form = ArticuloForm()
    return render(request, 'Articulo/crearArticuloPasoDG.html',{'form':form})

def comprobarEmailAutor(request,articulo_id):
    articulo = Articulo.objects.get(pk= articulo_id)
    if request.method == 'POST':
        form = CorreoForm(request.POST)
        if form.is_valid():
            correoA = form.cleaned_data['correo']
            if articulo.autores.filter(persona=correoA).exists():   
                error_message = 'Una persona con este correo ya es autor de este articulo'
                autores = articulo.autores.all()
                return render(request, 'Articulo/crearArticuloPasoAutor.html',{'correoForm':form,
                                                                               'error_message':error_message,
                                                                               'autores': autores,
                                                                               'articulo_id':articulo_id},)
            else:
                try:
                    personaA = Persona.objects.get(correo = correoA)
                    autor, autorCreado = Autor.objects.get_or_create(persona = personaA)
                    articulo.autores.add(autor)
                    autores = articulo.autores.all()
                    correoForm = CorreoForm()
                    return render(request, 'Articulo/crearArticuloPasoAutor.html', {'correoForm':correoForm,
                                                                                    'articulo_id':articulo_id,
                                                                                    'autores':autores})
                except Persona.DoesNotExist:
                    
                    autorForm = PersonaForm(initial={'correo':correoA})
                    autores = articulo.autores.all()
                    correoForm = CorreoForm()
                    return render(request,'Articulo/crearArticuloPasoAutor.html',{'autorForm':autorForm,
                                                                                  'correoForm':correoForm,
                                                                                  'autores':autores,
                                                                                  'articulo_id':articulo_id})
                else:
                    correoForm = CorreoForm()
                    autores=articulo.autores.all()
                    return render(request, 'Articulo/crearArticuloPasoAutor.html',{'correoForm':correoForm,
                                                                                   'autores':autores,
                                                                                   'articulo_id':articulo_id})
        else:
            correoForm = CorreoForm()
            autores=articulo.autores.all()
            return render(request,'Articulo/crearArticuloPasoAutor.html',{'correoForm':correoForm,
                                                                          'autores':autores,
                                                                        'articulo_id':articulo_id,
                                                                        'error_message':'Introduzca una direccion de correo valida'})
                     
def crearAutor(request,articulo_id):
    articulo = Articulo.objects.get(pk=articulo_id)
    formVacio = PersonaForm()
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        correoForm = CorreoForm()
        if form.is_valid():
            correoA = form.cleaned_data['correo']
            #    Si ya existe un autor con el correo ingresado relacionado con el articulo a crear, muestra un
            #    mensaje de error
            if articulo.autores.filter(persona=correoA).exists():

                error_message = 'Una persona con este correo ya es autor de este articulo'
                
                return render(request, 'Articulo/crearArticuloPasoAutor.html',{'correoForm':correoForm,
                                                                               'error_message':error_message,
                                                                               'articulo_id':articulo_id},)
            else:
                personaA, personaCreada = Persona.objects.get_or_create(
                                        correo=form.cleaned_data['correo'],
                                        defaults={'nombre':form.cleaned_data['nombre'],
                                                  'apellido':form.cleaned_data['apellido'],
                                                  'dirpostal':form.cleaned_data['dirpostal'],
                                                  'pagina':form.cleaned_data['pagina'],
                                                  'institucion':form.cleaned_data['institucion'],
                                                  'telefono':form.cleaned_data['telefono'],
                                                  'pais':form.cleaned_data['pais'],}
                                        )
                autor, autorCreado = Autor.objects.get_or_create(persona = personaA)
                articulo.autores.add(autor)
                autores = articulo.autores.all()
                return render(request, 'Articulo/crearArticuloPasoAutor.html',{'correoForm':correoForm,
                                                                               'autores':autores,
                                                                               'articulo_id':articulo_id,})
        autores = articulo.autores.all()
        return render(request, 'Articulo/crearArticuloPasoAutor.html',{ 'correoForm':correoForm,
                                                                        'autorForm':form,
                                                                        'articulo_id':articulo_id,
                                                                        'autores':autores})
def crearTopico(request, articulo_id):
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        articulo = Articulo.objects.get(pk = articulo_id)
        if form.is_valid():
            topico, topicoCreado= Topico.objects.get_or_create(nombre = form.cleaned_data['nombre'])
            
            topicos = articulo.topicos.all()
            if articulo.topicos.filter(nombre = form.cleaned_data['nombre']).exists():
                error_message = 'Ya existe este topico en la lista'
                return render(request, 'Articulo/crearArticuloPasoTopico.html',{'topicos':topicos,
                                                                            'articulo_id':articulo_id,
                                                                            'form':form,
                                                                            'error_message':error_message})
            articulo.topicos.add(topico)
            return render(request, 'Articulo/crearArticuloPasoTopico.html',{'topicos':topicos,
                                                                            'articulo_id':articulo_id,
                                                                            'form':form})
        else:
            topicos = articulo.topicos.all()
            form = TopicoForm()
            return render(request, 'Articulo/crearArticuloPasoTopico.html',{'topicos':topicos,
                                                                            'articulo_id': articulo_id,
                                                                            'form':form,})                                                                 