from Evento.models import Apertura,Clausura,Taller,Ponencia,CharlaInvitada, EventoSocial

def existe(tituloE):
        A=Apertura.objects.filter(titulo=tituloE).exists()
        C=Clausura.objects.filter(titulo=tituloE).exists()
        T=Taller.objects.filter(titulo=tituloE).exists()
        P=Ponencia.objects.filter(titulo=tituloE).exists()
        Ch=CharlaInvitada.objects.filter(titulo=tituloE).exists()
        E=EventoSocial.objects.filter(titulo=tituloE).exists()
        return A or C or T or P or Ch or E
    
def existeApertura():
    return Apertura.objects.filter(pk=1).exists()

def existeClausura():
    return Clausura.objects.filter(pk=1).exists()