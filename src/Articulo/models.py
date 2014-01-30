from django.db import models

from Autor.models import Autor
from Topico.models import Topico
from Evento.models import Ponencia, CharlaInvitada, Taller

class Articulo(models.Model):
    titulo = models.CharField(max_length=100)
    palabrasClaves= models.CharField(max_length=100)
    resumen = models.CharField(max_length=100)
    texto = models.CharField(max_length=300)
    autores = models.ManyToManyField(Autor, null = True)
    topicos = models.ManyToManyField(Topico, null =True)
    aceptado = models.BooleanField(default = False)
    aceptable = models.BooleanField(default = False)
    empatado = models.BooleanField(default = False)
    aceptadoEspecial = models.BooleanField(default = False)
    rechazadoFaltaCupo = models.BooleanField(default = False)
    rechazadoPorPromedio = models.BooleanField(default = False)
    perteneceAPotencia = models.ForeignKey(Ponencia, null = True)
    perteneceATaller = models.OneToOneField(Taller, null = True)
    perteneceACharlaInvitada = models.OneToOneField(CharlaInvitada, null = True)
    
    def __unicode__(self):
        return self.titulo
    
    