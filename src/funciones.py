from Persona.models import Persona
from Inscripcion.models import Inscripcion

def getPersona(correoF):
        try:
            per = Persona.objects.get(correo=correoF)
        except Persona.DoesNotExist:
            per = None 
        return per
    
def getInscripcion(correoF):
    try:
        ins = Inscripcion.objects.get(correo = correoF)
    except Inscripcion.DoesNotExist:
        ins = None
    return ins