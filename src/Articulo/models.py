from django.db import models

from Autor.models import Autor
from Topico.models import Topico

class Articulo(models.Model):
    titulo = models.CharField(max_length=100)
    palabrasClaves= models.CharField(max_length=100)
    resumen = models.CharField(max_length=100)
    texto = models.CharField(max_length=300)
    autores = models.ManyToManyField(Autor, null = True)
    topicos = models.ManyToManyField(Topico, null =True)
    
    def __unicode__(self):
        return self.titulo
    
    