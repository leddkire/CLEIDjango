from Persona.models import Persona
from Comite.models import Comite
from Invitado.models import Invitado

def getPersona(correoF):
        try:
            per = Persona.objects.get(correo=correoF)
        except Persona.DoesNotExist:
            per = None 
        return per
    
def getComite(correoF):
    try:
        com = Comite.objects.get(correo = correoF)
    except Comite.DoesNotExist:
        com = None
    return com

def getInvitado(correoF):
    try:
        inv = Invitado.objects.get(correo = correoF)
    except Invitado.DoesNotExist:
        inv = None
    return inv