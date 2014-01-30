from django.forms import ModelForm
from Comite.models import Comite, Moderador
from django import forms

from Persona.forms import PersonaForm 

class ComiteForm(ModelForm):
    
    class Meta:
        model = Comite
        fields = ['presidente', 'arbitro']
        
class CorreoForm(forms.Form):
    correo = forms.EmailField()
    
class PersonaComiteForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    correo = forms.EmailField()
    dirpostal = forms.IntegerField(min_value=0)
    institucion = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=100)
    pagina = forms.CharField(max_length=100)
    presidente = forms.BooleanField(initial=False, required = False)
    arbitro = forms.BooleanField(initial=False, required = False)

class ModeradorForm(forms.ModelForm):
    class Meta:
        model = Moderador
        fields = ['comite']