from django.db import models

from Persona.models import Persona

class Invitado(models.Model):
    correo = models.OneToOneField(Persona)
    cv = models.CharField(max_length=500)
    
    def __unicode__(self):
        return str(self.correo)+str(self.cv)