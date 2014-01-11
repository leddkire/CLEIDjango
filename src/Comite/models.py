from django.db import models

from Persona.models import Persona
# Create your models here.
class Comite(models.Model):
    correo = models.OneToOneField(Persona)
    presidente = models.BooleanField()
    arbitro = models.BooleanField()
    
    def __unicode__(self):
        return str(self.correo)

    