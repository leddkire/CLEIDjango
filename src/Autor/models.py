from django.db import models

from Persona.models import Persona

class Autor(models.Model):
    persona = models.OneToOneField(Persona)
