from Evento.models import Apertura,Clausura,Taller,Ponencia,CharlaInvitada, EventoSocial
from Lugar.models import Lugar
from datetime import timedelta, datetime, time

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

def noIntersectan(listaEventos, horaIni, horaFin):
    for evento in listaEventos:
        fechaHoraFinE = datetime.combine(evento.fechaIni,evento.horaIni)
        fechaHoraFinE = fechaHoraFinE + timedelta(hours = evento.duracion)
        horaFinE = time(fechaHoraFinE.hour,fechaHoraFinE.minute,fechaHoraFinE.second,fechaHoraFinE.microsecond)
        if evento.horaIni >= horaFin or horaFinE <= horaIni:
            return True
        else:
            return False
    return True
    

def intersectaFecha(fechaIniE,horaIniE,lugarE,duracionE):
    A = Apertura.objects.filter(lugar=lugarE).filter(fechaIni = fechaIniE)
    C = Clausura.objects.filter(lugar=lugarE).filter(fechaIni = fechaIniE)
    T = Taller.objects.filter(lugar=lugarE).filter(fechaIni = fechaIniE)
    P = Ponencia.objects.filter(lugar=lugarE).filter(fechaIni = fechaIniE)
    Ch = CharlaInvitada.objects.filter(lugar=lugarE).filter(fechaIni = fechaIniE)
    E = EventoSocial.objects.filter(lugar=lugarE).filter(fechaIni = fechaIniE)
    #Para calcular la hora de finalizacion del evento
    #se tiene que combinar la fecha con la hora
    fechaHoraIni = datetime.combine(fechaIniE,horaIniE)
    fechaHoraFin = fechaHoraIni + timedelta(hours=duracionE)
    horaFinE= time(fechaHoraFin.hour,fechaHoraFin.minute,fechaHoraFin.second,fechaHoraFin.microsecond)
    if (noIntersectan(A,horaIniE,horaFinE) and
       noIntersectan(C,horaIniE,horaFinE) and
       noIntersectan(T,horaIniE,horaFinE) and
       noIntersectan(P,horaIniE,horaFinE) and
       noIntersectan(Ch,horaIniE,horaFinE) and
       noIntersectan(E,horaIniE,horaFinE)):
        return False
    return True
     