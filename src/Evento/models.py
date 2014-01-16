from django.db import models
from Lugar.models import Lugar 
from Articulo.models import Articulo
from Comite.models import Moderador
from Topico.models import Topico


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
    articulo = models.OneToOneField(Articulo, null = True)
    topicos = models.ManyToManyField(Topico, null = True)
    def __unicode__(self):
        return self.titulo
    
class Ponencia(Evento):
    articulo = models.ForeignKey(Articulo, null = True)
    moderadores = models.ForeignKey(Moderador, null = True)
    topicos = models.ManyToManyField(Topico, null = True)
    def __unicode__(self):
        return self.titulo
    
class CharlaInvitada(Evento):
    articulos = models.OneToOneField(Articulo, null = True)
    moderadores = models.ForeignKey(Moderador, null = True)
    topicos = models.ManyToManyField(Topico, null = True)
    def __unicode__(self):
        return self.titulo