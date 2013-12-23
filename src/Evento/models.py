from django.db import models
from Lugar.models import Lugar 

class Evento(models.Model):
    lugar = models.ForeignKey(Lugar)
    titulo = models.CharField(max_length=100)
    duracion = models.PositiveIntegerField()
    fechaIni = models.DateField('fecha de inicio')
    horaIni = models.TimeField('hora de inicio')
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.titulo
    
class Apertura(Evento):
    
    def __unicode__(self):
        return self.titulo
    
class Clausura(Evento):
    
    def __unicode__(self):
        return self.titulo

class EventoSocial(Evento):
    
    def __unicode__(self):
        return self.titulo
    
class Taller(Evento):
    
    def __unicode__(self):
        return self.titulo
    
class Ponencia(Evento):
    
    def __unicode__(self):
        return self.titulo
    
class CharlaInvitada(Evento):
    
    def __unicode__(self):
        return self.titulo