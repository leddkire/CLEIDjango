from django.db import models
from Lugar.models import Lugar
from Comite.models import Moderador
from Topico.models import Topico


class Evento(models.Model):
    lugar = models.ForeignKey(Lugar)
    titulo = models.CharField(max_length=100)
    duracion = models.PositiveIntegerField("duracion (horas)")
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
    
    topico = models.ForeignKey(Topico,verbose_name = 'Topico principal')
    def __unicode__(self):
        return self.titulo
    
class Ponencia(Evento):
    moderadores = models.ManyToManyField(Moderador, null = True)
    topico = models.ForeignKey(Topico,verbose_name = 'Topico principal')
    def __unicode__(self):
        return self.titulo
    
class CharlaInvitada(Evento):
    moderadores = models.ManyToManyField(Moderador, null = True)
    topico = models.ForeignKey(Topico, verbose_name = 'Topico principal')
    def __unicode__(self):
        return self.titulo