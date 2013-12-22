from django.db import models
from Articulo.models import Articulo 

    
class Arbitro(models.Model):
    correo= models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.correo
    
class  Evaluacion(models.Model):
    NOTAS_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    )
    articulo = models.OneToOneField(Articulo)
    notas = models.IntegerField(choices=NOTAS_CHOICES)
    arbitros = models.ManyToManyField(Arbitro)
    promedio= models.FloatField()
    
    def __unicode__(self):
        return self.arbitros
        
