from django.db import models
import datetime

class Conferencia(models.Model):
    
    #Se inicializan los anios que se usaran como opciones.
    anioOpciones = []
    for r in range(1980, (datetime.datetime.now().year+2)):
        anioOpciones.append((r,r))
         
    
    anio = models.PositiveIntegerField(('anio'), max_length=4, choices=anioOpciones, default=datetime.datetime.now().year)
    pais = models.CharField(max_length=100)
    maxArticulos = models.PositiveIntegerField('maximo de articulos para aceptar')
    
    def __unicode__(self):
        return str(self.anio)
