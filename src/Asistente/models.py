from django.db import models

# Create your models here.
from Persona.models import Persona

class Asistente(models.Model):
    persona = models.OneToOneField(Persona)