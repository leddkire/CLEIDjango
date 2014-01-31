from Persona.models import Persona
from Comite.models import Comite
from Topico.models import Topico
from Invitado.models import Invitado
from Articulo.models import Articulo
from Evaluacion.models import Evaluacion
from Conferencia.models import Conferencia
from Inscripcion.models import Inscripcion
from django.db.models import Q
from Autor.models import Autor

#
# Archivo que contiene las consultas mas comunes a la base de datos, que pueden utilizar todas las
# aplicaciones.
#

#
# Funcion que devuelve una persona con corre = correoF.
#

def getPersona(correoF):
        try:
            per = Persona.objects.get(correo=correoF)
        except Persona.DoesNotExist:
            per = None 
        return per
#
# Funcion que devuelve el autor con correo = correoF.
#    
def getAutor(correoF):
    try:
        autor = Autor.objects.get(correo = correoF)
    except Autor.DoesNotExist:
        autor = None
    return autor

#
# Funcion que devuelve el miembro del comite con correo = correoF.
#    
def getComite(correoF):
    try:
        com = Comite.objects.get(correo = correoF)
    except Comite.DoesNotExist:
        com = None
    return com
#
# Funcion que devuelve la persona invitada con correo = correoF.
#
def getInvitado(correoF):
    try:
        inv = Invitado.objects.get(correo = correoF)
    except Invitado.DoesNotExist:
        inv = None
    return inv

#
# Funcion que devuelve la cantidad de articulos para determinado topico
#
def getNumArticulosDeTopico(topico):
    count = 0
    aceptados = getArticulosAceptadosYEspeciales()
    if aceptados != None:
        for articulo in aceptados:
            try:
                articulo.topicos.get(nombre = topico)
                count += 1
            except Topico.DoesNotExist:
                pass
    return count            

#
# Funcion que devuelve todos los topicos
#
def getTopicos():
    try:
        topicos = Topico.objects.all()
        if len(topicos) == 0:
            topicos = None
    except Topico.DoesNotExist:
        topicos = none
    return topicos

#
# Funcion que devuelve todos articulos
#
def getArticulosNoEspeciales():
    try:
        articulo = Articulo.objects.filter(aceptadoEspecial = False, aceptado = False)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos aceptados.
#

def getEventos():
    try:
        evento = Evento.objects.get(titulo = titulo)
    except Evento.DoesNotExist:
        evento = None
    return evento
            
#
# Funcion que devuelve todos los articulos aceptados.
#
def getArticulosAceptados():
    try:
        articulo = Articulo.objects.filter(aceptado = True)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

def getArticulosAceptadosYEspeciales():
    try:
        articulo = Articulo.objects.filter(Q(aceptado = True) | Q(aceptadoEspecial = True))
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos aceptados especiales.
#
def getArticulosAceptadosEspecial():
    try:
        articulo = Articulo.objects.filter(aceptadoEspecial = True)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos rechazados por falta de cupo.
#
def getArticulosRechazadosCupo():
    try:
        articulo = Articulo.objects.filter(rechazadoFaltaCupo = True)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo
# Funcion que devuelve todos los articulos rechazados por promedio.
#
def getArticulosRechazadosPorPromedio():
    try:
        articulo = Articulo.objects.filter(rechazadoPorPromedio = True)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos aceptados especiales.
#
def getArticulosAceptadosEspecial():
    try:
        articulo = Articulo.objects.filter(aceptadoEspecial = True)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos aceptables.
#
def getArticulosAceptables():
    try:
        articulo = Articulo.objects.filter(aceptable = True)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos aceptables.
#
def getArticulosEmpatados():
    try:
        articulo = Articulo.objects.filter(empatado = True)
        if len(articulo) == 0:
            articulo = None
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve el articulo con clave = id.
#
def getArticuloPorId(id):
    try:
        articulo = Articulo.objects.get(pk = id)
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve las evaluaciones para el articulo con clave = id.
#
def getEvaluacionesDeArticulo(id):
    try:
        evaluaciones = Evaluacion.objects.get(articulo = id)
    except Evaluacion.DoesNotExist:
        evaluaciones = None
    return evaluaciones

#
#
#
def getDatosConferencia():
    try:
        conferencia = Conferencia.objects.get()
        if conferencia:
            return conferencia.maxArticulos
    except Conferencia.DoesNotExist:
        conferencia = None
        return 0
   
def getInscripcion(correoF):
    try:
        ins = Inscripcion.objects.get(correo = correoF)
    except Inscripcion.DoesNotExist:
        ins = None
    return ins

