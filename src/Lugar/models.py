from django.db import models

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length = 200)
    capacidadMax = models.PositiveIntegerField()

    def __unicode__(self):
        return self.nombre

