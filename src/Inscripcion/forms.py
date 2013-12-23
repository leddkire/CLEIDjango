from django.forms import ModelForm
from django import forms

from Inscripcion.models import Inscripcion
from Persona.forms import PersonaForm 

class InscripcionForm(ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['correo']
        
class CorreoForm(forms.Form):
    correo = forms.EmailField()
       
class PersonaInscripcionForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    correo = forms.EmailField()
    dirpostal = forms.IntegerField(min_value=0)
    institucion = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=100)
    pagina = forms.CharField(max_length=100)
