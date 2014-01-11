from django.db import models

from Persona.models import Persona

# Create your models here.

class Inscripcion(models.Model):
    correo = models.OneToOneField(Persona)
    tarifa = models.PositiveIntegerField()
    fechainscripcion = models.DateField('fecha de inscripcion')
    fechatope = models.DateField('fecha tope')

    def __unicode__(self):
        return str(self.correo)
