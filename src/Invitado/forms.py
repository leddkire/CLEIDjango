from django.forms import ModelForm
from Invitado.models import Invitado
from django import forms

from Persona.forms import PersonaForm 

class InvitadoForm(ModelForm):
    
    class Meta:
        model = Invitado
        fields = ['cv']
    
class PersonaInvitadoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    correo = forms.EmailField()
    dirpostal = forms.IntegerField(min_value=0)
    institucion = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=100)
    pagina = forms.CharField(max_length=100)
    cv = forms.CharField(max_length=500)