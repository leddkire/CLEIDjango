from django.forms import ModelForm
from Conferencia.models import Conferencia
from django import forms

from Persona.forms import PersonaForm 

class ConferenciaForm(ModelForm):
    
    class Meta:
        model = Conferencia
        fields = ['anio', 'pais', 'maxArticulos']

