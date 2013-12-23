from Persona.models import Persona
from Comite.models import Comite
from Invitado.models import Invitado
from Articulo.models import Articulo
from Evaluacion.models import Evaluacion
from Conferencia.models import Conferencia
from Inscripcion.models import Inscripcion

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
# Funcion que devuelve todos los articulos aceptados.
#
def getArticulosAceptados():
    try:
        articulo = Articulo.objects.filter(aceptado = True)
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos aceptables.
#
def getArticulosAceptables():
    try:
        articulo = Articulo.objects.filter(aceptable = True)
    except Articulo.DoesNotExist:
        articulo = None
    return articulo

#
# Funcion que devuelve todos los articulos aceptables.
#
def getArticulosEmpatados():
    try:
        articulo = Articulo.objects.filter(empatado = True)
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

