from django.db import models

class Articulo(models.Model):
    titulo = models.CharField(max_length=100)
    palabrasClaves= models.CharField(max_length=50)
    resumen = models.CharField(max_length=100)
    texto = models.CharField(max_length=300)
    
    def __unicode__(self):
        return self.titulo
    
    