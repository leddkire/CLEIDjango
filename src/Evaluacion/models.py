from django.db import models
from Articulo.models import Articulo 
from Comite.models import Comite

NOTAS_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    )
class Arbitro(models.Model):
    correo= models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.correo
    
class Nota(models.Model):
    valor=models.IntegerField(choices=NOTAS_CHOICES)
    
    def __unicode__(self):
        return str(self.valor)
    
class  Evaluacion(models.Model):
    
    articulo = models.OneToOneField(Articulo)
    notas = models.ManyToManyField(Nota,unique=False)
    arbitros = models.ManyToManyField(Comite)
    promedio= models.FloatField(default=0.0)
    
    def __unicode__(self):
        return str(self.articulo)#.__unicode__()
        
