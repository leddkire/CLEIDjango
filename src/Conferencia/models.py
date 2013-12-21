from django.db import models
import datetime

class Conferencia(models.Model):
    
    #Se inicializan los anios que se usaran como opciones.
    anioOpciones = []
    for r in range(1980, (datetime.datetime.now().year+2)):
        anioOpciones.append((r,r))
         
    
    anio = models.IntegerField(('anio'), max_length=4, choices=anioOpciones, default=datetime.datetime.now().year)
    duracion = models.IntegerField()
    pais = models.CharField(max_length=100)
    maxArticulos = models.IntegerField()
    
    def __unicode__(self):
        return str(self.anio)
