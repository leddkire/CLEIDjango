from django.db import models

from Topico.models import Topico
from Persona.models import Persona
# Create your models here.
class Comite(models.Model):
    correo = models.OneToOneField(Persona)
    presidente = models.BooleanField()
    arbitro = models.BooleanField()
    topicos = models.ManyToManyField(Topico)
    
    def __unicode__(self):
        return str(self.correo)
    
class Moderador(models.Model):
    comite = models.OneToOneField(Comite)

    