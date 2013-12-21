from django.db import models

# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    dirpostal = models.IntegerField()
    institucion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    pagina = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nombre and self.apellido and self.correo
    
class Participante(Persona):

    def __unicode__(self):
        return self.nombre and self.apellido and self.correo
