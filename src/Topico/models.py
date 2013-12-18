from django.db import models

class Topico(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nombre